from sqlalchemy import select, update, delete, insert
from sqlalchemy.sql import ClauseElement
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Generic, TypeVar, Type, Any


from model import Habr
from database import async_session_maker

T = TypeVar("T")


class BaseDAO(Generic[T]):
    """Базовый класс взаимодействия с данными."""
    
    model: Type[T]
    
    @classmethod
    async def _find_all_data(
        cls, 
        *conditions: ClauseElement,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[T]:
        """
        Находит книги из бд.

        Args:
            limit: сколько книг вывести.
            offset: с какого места начать.
        """
        async with async_session_maker() as session:
            query = select(cls.model)
            if conditions:
                query = query.where(*conditions)
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            result = await session.execute(query)
            return list(result.scalars().all())

    @classmethod
    async def _add_data(cls, **values) -> None:
        """
        Добавляет данные в базу данных.

        Args:
            values: словарь с данными для добавления.
                    
                    Ключи должны соответствовать атрибутам ORM-модели.
                    Допустимый набор полей определяется конкретным DAO.
        
        Raises:
            IntegrityError - если добавляются данные, которые уже есть в базе.
            SQLAlchemyError - если возникла ошибка при добавлении.
            TypeError - если были переданы некорректные значения.
        """

        async with async_session_maker() as session:
            query = insert(cls.model).values(**values)
            try:
                await session.execute(query)
                await session.commit()
            except (TypeError, IntegrityError, SQLAlchemyError) as error:
                await session.rollback()
                raise error

    
class HabrDao(BaseDAO[Habr]):

    model = Habr

    @classmethod
    async def add_data(
        cls,
        title,
        author,
        publish_date,
        url
    ) -> None:
        
        await super()._add_data(
            title=title,
            author=author,
            publish_date=publish_date,
            url=url
        )
    
    @classmethod
    async def find_data(
        cls,
        limit,
        offset
    ) -> list[Habr]:

        return await super()._find_all_data(
            limit=limit,
            offset=offset
        )
    