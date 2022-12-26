import uuid
import datetime as dt

from typing import Optional, Union, Tuple
from bson.binary import Binary

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, Request, Query

from src.services.views import Views
from src.db.mongodb import get_mongo
from src.models.models import FilmLikeAPI, FilmLike
from src.utils.abstract_db import AbstractDB, MongoDB
from src.core.config import settings


class FilmLikeService(Views):
    def __init__(self, mongo: AbstractDB):
        self.db = mongo

    async def add_film_like(self, user_id: uuid.UUID, film_id: uuid.UUID, value: int):
        """
        Добавление лайка фильма

        @param value: Оценка фильма
        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        """
        film_like_exists = await self.__check_film_like(user_id, film_id)
        if film_like_exists:
            return None
        film_like = FilmLike(film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
                             user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
                             value=value,
                             added_at=dt.datetime.today())
        added_film_like = await self.insert_record(
            collection=settings.mongo_likes_collection,
            document=film_like.dict()
        )
        return added_film_like


    async def delete_film_like(self, user_id: uuid.UUID, film_id: uuid.UUID):
        """
        Удаление лайка фильма

        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        """
        film_like_exists = await self.__check_film_like(user_id, film_id)
        if not film_like_exists:
            return None
        removed_film_like = await self.delete_record(
            collection=settings.mongo_likes_collection,
            film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
        )
        return removed_film_like


    async def update_film_like(self, user_id: uuid.UUID, film_id: uuid.UUID, value: int):
        """
        Обновление лайка фильма

        @param value: новое значение оценки пользователя
        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        """
        film_like_exists = await self.__check_film_like(user_id, film_id)
        if not film_like_exists:
            return None
        updated_film_like = await self.update_record(
            collection=settings.mongo_likes_collection,
            film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
            new_document=FilmLike(
                film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
                user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
                added_at=dt.datetime.now(),
                value=value
            ).dict()
        )
        return updated_film_like


    async def average_film_likes(self, film_id: uuid.UUID):
        """
        Нахождение среднего значения рейтинга фильма

        @param film_id: uuid фильма
        """
        average_likes = await self.record_average(
            collection=settings.mongo_likes_collection,
            expression=[
                {
                    "$match": {"film_id": bytes(Binary.from_uuid(uuid.UUID(film_id)))}
                },
                {
                    "$group": {"_id": "$film_id", "average_rating:": { "$avg": "$value"}}
                }
            ]
        )

        return average_likes


    async def summary_film_likes(self, film_id: uuid.UUID):
        """
        Вывод информации о количестве проставленных оценок фильму

        @param film_id: uuid фильма
        """
        dislikes = await self.record_count(
            collection=settings.mongo_likes_collection,
            expression={
                "film_id": bytes(Binary.from_uuid(uuid.UUID(film_id))),
                "value": {'$lte': 3}
            }
        )

        normal = await self.record_count(
            collection=settings.mongo_likes_collection,
            expression={
                "film_id": bytes(Binary.from_uuid(uuid.UUID(film_id))),
                "value": {"$gt": 3, "$lt": 8}
            }
        )

        likes = await self.record_count(
            collection=settings.mongo_likes_collection,
            expression={
                "film_id": bytes(Binary.from_uuid(uuid.UUID(film_id))),
                "value": {'$gte': 8}
            }
        )

        summary_likes = {
            "dislikes, 0-3": dislikes,
            "normal, 4-7": normal,
            "likes, 8-10": likes
        }

        return summary_likes


    async def __check_film_like(self, user_id: uuid.UUID, film_id: uuid.UUID):
        """
        Проверка наличия фильма

        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        """
        film_like = await self.check_record(
            collection=settings.mongo_likes_collection,
            film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
        )
        return film_like


def get_film_like_service(
        mongo: AsyncIOMotorClient = Depends(get_mongo),
) -> FilmLikeService:
    """
    Провайдер FilmLikeService,
    с помощью Depends он сообщает, что ему необходим MongoDB
    """
    return FilmLikeService(MongoDB(mongo))
