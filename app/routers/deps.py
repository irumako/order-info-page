from collections.abc import AsyncGenerator

from database import AsyncSessionFactory


class PaginationParams:
    def __init__(self, page: int = 1, step: int = 3):
        self.page = page
        self.step = step

    def get_total_pages(self, sequence_len):
        total_pages = sequence_len // self.step
        total_pages += 1 if sequence_len % self.step > 0 else 0
        return total_pages

    def get_current_page(self, total_pages):
        current_page = min(range(1, total_pages + 1), key=lambda x: abs(x - self.page))
        return current_page


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
