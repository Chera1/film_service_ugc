import sys
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT
from motor.motor_asyncio import AsyncIOMotorClient

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.api.v1 import bookmark, like, review
from src.core.config import settings
from src.db import mongodb

# Создание FastAPI приложения
app = FastAPI(
    title='name',
    description="API для работы с лайками, закладками и рецензиями к фильмам пользователей",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    version='1.0.0'
)


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return settings


@app.on_event('startup')
async def startup():
    # Подключаемся к базам при старте сервера
    mongodb.mongo = AsyncIOMotorClient(settings.mongo_host, settings.mongo_port)


@app.on_event("shutdown")
async def shutdown_event():
    await mongodb.mongo.close()


# Подключаем роутеры
app.include_router(bookmark.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
app.include_router(like.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(review.router, prefix='/api/v1/reviews', tags=['reviews'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.service_host,
        port=settings.service_port,
    )
