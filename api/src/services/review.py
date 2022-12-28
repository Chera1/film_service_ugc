import uuid
import datetime as dt

from typing import Optional, Union, Tuple
from bson.binary import Binary

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, Request, Query

from src.services.views import Views
from src.db.mongodb import get_mongo
from src.models.models import ReviewAPI, Review, ReviewLikeAPI, ReviewLike
from src.utils.abstract_db import AbstractDB, MongoDB
from src.core.config import settings


class ReviewService(Views):
    def __init__(self, mongo: AbstractDB):
        self.db = mongo

    async def add_review(self, user_id: uuid.UUID, film_id: uuid.UUID, text: str):
        """
        Добавление рецензии на фильм

        @param text: Текст рецензии
        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        """
        review_exists = await self.__check_review(user_id, film_id)
        if review_exists:
            return None
        review = Review(film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
                        user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
                        text=text,
                        published_at=dt.datetime.today())
        added_film_like = await self.insert_record(
            collection=settings.mongo_reviews_collection,
            document=review.dict()
        )
        return added_film_like


    async def add_like_to_review(self, user_id: uuid.UUID, review_id: str, value: int):
        """
        Добавление лайка к рецензии на фильм

        @param value: Значение лайка
        @param user_id: uuid пользователя
        @param review_id: id рецензии
        """
        review_exists = await self.__check_review_by_id(review_id)
        if review_exists:
            return None
        review = ReviewLike(review_id=review_id,
                            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
                            value=value,
                            added_at=dt.datetime.today())
        added_review_like = await self.insert_record(
            collection=settings.mongo_reviews_likes_collection,
            document=review.dict()
        )
        return added_review_like


    async def get_reviews(
            self,
            sort: Optional[str] = None,
            limit: Optional[int] = 50,
            page: Optional[int] = 1,
    ):
        """
        Получение списка рецензий

        @param sort: поле для сортировки
        @param limit: количество записей на странице
        @param page: номер страницы
        """
        sort = sort.split('&')
        sort_string = []

        for item in sort:
            if item[0] == '-':
                sort_string.append((item[1:], -1))
            else:
                sort_string.append((item, 1))

        reviews = await self.get_records(
            collection=settings.mongo_reviews_collection,
            sort=sort_string,
            limit=limit,
            page=page
        )

        reviews = (ReviewAPI(id=str(review['_id']),
                             film_id=str(uuid.UUID(bytes=review['film_id'])),
                             user_id=str(uuid.UUID(bytes=review['user_id'])),
                             text=review['text'],
                             published_at=str(review['published_at']))
                   for review in reviews)
        return reviews


    async def __check_review(self, user_id: uuid.UUID, film_id: uuid.UUID):
        """
        Проверка наличия рецензии

        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        @return:
        """
        review = await self.check_record(
            collection=settings.mongo_reviews_collection,
            film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
        )
        return review


    async def __check_review_by_id(self, _id: str):
        """
        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        @return:
        """
        review = await self.check_record_by_id(
            collection=settings.mongo_reviews_collection,
            _id=_id,
        )
        return review


def get_review_service(
        mongo: AsyncIOMotorClient = Depends(get_mongo),
) -> ReviewService:
    """
    Провайдер FilmLikeService,
    с помощью Depends он сообщает, что ему необходим MongoDB
    """
    return ReviewService(MongoDB(mongo))
