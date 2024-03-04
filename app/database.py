from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import settings


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI.unicode_string(),
    future=True,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)
