from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

URL_DB = settings.async_database_url
async_engine = create_async_engine(URL_DB, echo=True)


class Base(DeclarativeBase):
    pass


async_session = async_sessionmaker(async_engine, expire_on_commit=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
