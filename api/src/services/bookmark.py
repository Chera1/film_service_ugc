import uuid
import datetime as dt

from typing import Optional, Union, Tuple
from bson.binary import Binary

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, Request, Query

from src.services.views import Views
from src.db.mongodb import get_mongo
from src.models.models import Bookmark, BookmarkAPI
from src.utils.abstract_db import AbstractDB, MongoDB
from src.core.config import settings


class BookMarkService(Views):
    def __init__(self, mongo: AbstractDB):
        self.db = mongo

    async def add_bookmark(self, user_id: uuid.UUID, film_id: uuid.UUID):
        """
        Добавление закладки

        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        """
        bookmark_exists = await self.__check_bookmark(user_id, film_id)
        if bookmark_exists:
            return None
        bookmark = Bookmark(film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
                            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
                            added_at=dt.datetime.today())
        added_bookmark = await self.insert_record(
            collection=settings.mongo_bookmarks_collection,
            document=bookmark.dict()
        )
        return added_bookmark


    async def delete_bookmark(self, user_id: uuid.UUID, film_id: uuid.UUID):
        """
        Удаление закладки

        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        """
        bookmark_exists = await self.__check_bookmark(user_id, film_id)
        if not bookmark_exists:
            return None
        removed_bookmark = await self.delete_record(
            collection=settings.mongo_bookmarks_collection,
            film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
        )
        return removed_bookmark


    async def get_bookmarks(self, user_id: uuid.UUID):
        """
        Выборка закладок пользователя

        @param user_id: uuid пользователя
        """
        bookmarks = await self.get_records(
            collection=settings.mongo_bookmarks_collection,
            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
        )
        bookmarks = (BookmarkAPI(id=str(bookmark['_id']),
                                 film_id=str(uuid.UUID(bytes=bookmark['film_id'])),
                                 user_id=str(uuid.UUID(bytes=bookmark['user_id'])),
                                 added_at=str(bookmark['added_at']))
                     for bookmark in bookmarks)
        return bookmarks


    async def __check_bookmark(self, user_id: uuid.UUID, film_id: uuid.UUID):
        """
        Проверка наличия закладки

        @param user_id: uuid пользователя
        @param film_id: uuid фильма
        @return:
        """
        bookmark = await self.check_record(
            collection=settings.mongo_bookmarks_collection,
            film_id=bytes(Binary.from_uuid(uuid.UUID(film_id))),
            user_id=bytes(Binary.from_uuid(uuid.UUID(user_id))),
        )
        return bookmark


def get_bookmark_service(
        mongo: AsyncIOMotorClient = Depends(get_mongo),
) -> BookMarkService:
    """
    Провайдер BookMarkService,
    с помощью Depends он сообщает, что ему необходим MongoDB
    """
    return BookMarkService(MongoDB(mongo))
