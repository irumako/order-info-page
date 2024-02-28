from collections.abc import AsyncGenerator

from database import AsyncSessionFactory


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
