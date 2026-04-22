from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Базовая ORM-модель."""

    __abstract__ = True


class Habr(Base):
    """ORM-модель таблицы habr."""

    __tablename__ = "habr"
    _table_args__ = {"schema": "public"}  

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    publish_date: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()

    extend_existing = True