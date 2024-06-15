from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

DATABASE_PARAMS = {"poolclass": NullPool}

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
else:
    DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


# Используется для миграций
class Base(DeclarativeBase):
    pass


engine_nullpool = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
# Создаем async_session_maker с движком NullPool
async_session_maker_nullpool = async_sessionmaker(bind=engine_nullpool, expire_on_commit=False)
