from os import getenv 
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import pool


load_dotenv()


def get_database_url() -> str:
    """
    Формирует URL для асинхронного соединения с базой данных.
     
    Returns:
        Строка-url для асинхронного соединения с базой данных.
    """

    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    name = getenv("DB_NAME")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


DB_URL = get_database_url()


async_engine = create_async_engine(DB_URL, poolclass=pool.NullPool)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)