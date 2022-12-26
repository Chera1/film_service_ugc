import uuid

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, Any, Union

from src.utils.abstract_db import AbstractDB


class AbstractViewEngine(ABC):
    """
    Абстрактный класс для реализации отдачи данных сервисом
    """

    @abstractmethod
    def get_records(self, collection, user_id):
        pass

    @abstractmethod
    def insert_record(self, collection, document):
        pass

    @abstractmethod
    def update_record(self, collection, film_id, user_id, new_document):
        pass

    @abstractmethod
    def delete_record(self, collection, film_id, user_id):
        pass

    @abstractmethod
    def check_record(self, collection, film_id, user_id):
        pass


@dataclass
class Views(AbstractViewEngine):
    db: AbstractDB

    async def get_records(
            self,
            collection: str,
            user_id: Optional[uuid.UUID] = None,
            sort: Optional[str] = None,
            limit: Optional[int] = 50,
            page: Optional[int] = 1,
    ) -> Union[list, None]:
        """
        Получаем документы по uuid пользователя

        @param user_id: uuid пользователя
        @param collection: Запрашиваемая коллекция
        @param sort: поле для сортировки
        @param limit: количество записей на странице
        @param page: номер страницы
        @return: список документов
        """
        records = await self.db.get(
            collection,
            user_id,
            sort,
            limit,
            page
        )

        return records


    async def check_record(
            self,
            collection: str,
            user_id: uuid.UUID,
            film_id: uuid.UUID,
    ) -> bool:
        """
        Получаем документы по uuid пользователя

        @param film_id: uuid фильма
        @param user_id: uuid пользователя
        @param collection: Запрашиваемая коллекция
        @return: список документов
        """
        record = await self.db.get_one(collection, film_id, user_id)

        return True if record else False


    async def check_record_by_id(
            self,
            collection: str,
            _id: str,
    ) -> bool:
        """
        Проверка наличия документа по id

        @param _id: id документа в коллекции
        @param collection: Запрашиваемая коллекция
        @return: список документов
        """
        record = await self.db.get_by_id(collection, _id)

        return True if record else False


    async def insert_record(
            self,
            collection: str,
            document: dict
    ) -> Any:
        """
        Вставка документа в коллекцию

        @param document: вставляемый домумент
        @param collection: Запрашиваемая коллекция
        """
        record = await self.db.insert(collection, document)

        return record


    async def delete_record(
            self,
            collection: str,
            film_id: uuid.UUID,
            user_id: uuid.UUID
    ) -> Any:
        """
        Удаление документа из коллекции

        @param collection: Запрашиваемая коллекция
        @param film_id: uuid фильма
        @param user_id: uuid пользователя
        """
        record = await self.db.delete(collection, film_id, user_id)

        return record


    async def update_record(
            self,
            collection: str,
            film_id: uuid.UUID,
            user_id: uuid.UUID,
            new_document: dict
    ) -> Any:
        """
        Удаление документа из коллекции

        @param new_document: новый документ, который заменяет старый
        @param collection: Запрашиваемая коллекция
        @param film_id: uuid фильма
        @param user_id: uuid пользователя
        """
        record = await self.db.update(collection, film_id, user_id, new_document)

        return record


    async def record_average(
            self,
            collection: str,
            expression: Union[dict, list[dict]]
    ) -> Any:
        """
        Агрегация данных из коллекции по выражению

        @param expression: Выражение для агрегации
        @param collection: Запрашиваемая коллекция
        """
        record = await self.db.aggregate(collection, expression)

        return record


    async def record_count(
            self,
            collection: str,
            expression: Union[dict, list[dict]]
    ) -> Any:
        """
        Подсчет записей в коллекции по условию

        @param expression: Выражение для агрегации
        @param collection: Запрашиваемая коллекция
        """
        record = await self.db.count(collection, expression)

        return record
