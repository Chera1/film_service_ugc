from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Конфиг сервиса"""

    service_host: str = Field('localhost', env='SERVICE_HOST')
    service_port: int = Field(8000, env='SERVICE_PORT')

    # authjwt_secret_key должен совпадать с сервисом авторизации
    authjwt_secret_key: str = Field(..., env='SERVICE_SECRET_KEY')

    sentry_dsn: str = Field(..., env='SENTRY_DSN')

    mongo_host: str = Field('localhost', env='MONGO_HOST')
    mongo_port: int = Field('5660', env='MONGO_PORT')
    mongo_user: str = Field(..., env='MONGO_USER')
    mongo_passwd: str = Field(..., env='MONGO_PASSWD')
    mongo_db: str = Field(..., env='MONGO_DB')
    mongo_likes_collection: str = Field(..., env='MONGO_LIKES')
    mongo_bookmarks_collection: str = Field(..., env='MONGO_BOOKMARKS')
    mongo_reviews_collection: str = Field(..., env='MONGO_REVIEWS')
    mongo_reviews_likes_collection: str = Field(..., env='MONGO_REVIEWS_LIKES')

    class Config:
        env_file = "src/core/.env"
        env_file_encoding = "utf-8"


settings = Settings()
