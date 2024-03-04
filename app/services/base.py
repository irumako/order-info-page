from pydantic import BaseModel

from repositories.base import BaseRepository
from utils import parse_pydantic_schema, is_pydantic


class BaseService:

    def __init__(self, repository: BaseRepository) -> None:
        self.repository: BaseRepository = repository

    async def create(self, model: BaseModel) -> BaseModel:
        return await self.repository.create(data=parse_pydantic_schema(dict(model)))

    async def update(self, pk: int, model: BaseModel) -> BaseModel:
        return await self.repository.update(data=parse_pydantic_schema(dict(model)), id=pk)

    async def delete(self, pk: int) -> None:
        await self.repository.delete(id=pk)

    async def get(self, pk: int) -> BaseModel:
        return await self.repository.get_single(id=pk)
