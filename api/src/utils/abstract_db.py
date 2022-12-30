import uuid

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union, List, Any, Optional

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings


class AbstractDB(ABC):
    """
    Абстрактный класс для реализации работы с хранилищем
    """

    @abstractmethod
    def insert(self, collection, document):
        pass

    @abstractmethod
    def get(self, collection, user_id):
        pass

    @abstractmethod
    def get_one(self, collection, content_id, user_id):
        pass

    @abstractmethod
    def delete(self, collection, film_id, user_id):
        pass

    @abstractmethod
    def update(self, collection, film_id, user_id, new_document):
        pass

    @abstractmethod
    def aggregate(self, collection, expression):
        pass

    @abstractmethod
    def count(self, collection, expression):
        pass


@dataclass
class MongoDB(AbstractDB):
    """
    Класс для обращений к MongoDB
    """
    mongo: AsyncIOMotorClient

    async def insert(self, collection: str, document: dict):
        """
        Вставка документа в коллекцию

        Args:
            collection: запрашиваемая коллекция
            document: документ
        Returns:
            response: Список документов
        """
        document = await self.mongo[settings.mongo_db][collection].insert_one(document)
        return document


    async def get(self,
                  collection: str,
                  user_id: Optional[uuid.UUID] = None,
                  sort: Optional[str] = None,
                  limit: Optional[int] = 50,
                  page: Optional[int] = 1,
                  ) -> Union[list, None]:
        """
        Получение списка документов по id пользователя

        Args:
            collection: запрашиваемая коллекция
            user_id: id пользователя
            sort: поле для сортировки
            limit: количество записей на странице
            page: номер страницы
        Returns:
            response: Список документов
        """
        expression = {}
        if user_id:
            expression["user_id"] = user_id
        documents = await self.mongo[settings.mongo_db][collection].find(
            expression, sort=sort).limit(limit).skip((page - 1) * limit).to_list(length=200)
        return documents


    async def get_one(self, collection: str, film_id: uuid.UUID, user_id: uuid.UUID) -> Any:
        """
        Получение одного документа по заданному условию

        Args:
            collection: запрашиваемая коллекция
            user_id: id пользователя
            film_id: id фильма
        Returns:
            response: Искомый документ
        """
        expression = {
            'user_id': user_id,
            'film_id': film_id
        }
        document = await self.mongo[settings.mongo_db][collection].find_one(expression)
        return document


    async def get_by_id(self, collection: str, _id: str) -> Any:
        """
        Получение одного документа по заданному условию

        Args:
            collection: запрашиваемая коллекция
            _id: id документа в коллекции
        Returns:
            response: Искомый документ
        """
        expression = {
            '_id': _id
        }
        document = await self.mongo[settings.mongo_db][collection].find_one(expression)
        return document


    async def delete(self, collection: str, film_id: uuid.UUID, user_id: uuid.UUID):
        """
        Удаление документа из коллекции

        Args:
            collection: запрашиваемая коллекция
            user_id: id пользователя
            film_id: id фильма
        """
        expression = {
            'user_id': user_id,
            'film_id': film_id
        }
        document = await self.mongo[settings.mongo_db][collection].delete_one(expression)
        return document


    async def update(self, collection: str,
                     film_id: uuid.UUID,
                     user_id: uuid.UUID,
                     new_document: dict) -> Any:
        """
        Обновление документа в коллекции

        Args:
            collection: запрашиваемая коллекция
            user_id: id пользователя
            film_id: id фильма
            new_document: новый документ
        """
        expression = {
            'user_id': user_id,
            'film_id': film_id
        }
        document = await self.mongo[settings.mongo_db][collection].update_one(
            expression,
            {'$set': new_document})
        return document


    async def aggregate(self, collection: str, expression: Union[dict, list[dict]]):
        """
            Обновление документа в коллекции

            Args:
                collection: запрашиваемая коллекция
                expression: выражение для агрегации
        """
        result = await self.mongo[settings.mongo_db][collection].aggregate(
            expression).to_list(length=200)

        return result


    async def count(self, collection: str, expression: Union[dict, list[dict]]):
        """
            Подсчет документов в коллекции по условию

            Args:
                collection: запрашиваемая коллекция
                expression: выражение для агрегации
        """
        result = await self.mongo[settings.mongo_db][collection].count_documents(
            expression)

        return result
