from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import Field, field_validator

from .base import Base
from .product import Product


class Order(Base):
    id: str = Field(max_length=16, validation_alias="Номер")
    date: datetime = Field(validation_alias="Дата")
    contractor: str = Field(max_length=100, validation_alias="Контрагент")
    amount: Decimal = Field(max_digits=12, decimal_places=2, validation_alias="Сумма")

    products: List[Product] = Field(validation_alias="Товары")

    @field_validator("date", mode="before")
    def parse_order_date(cls, value):
        return datetime.strptime(
            value,
            "%Y%m%d"
        ).date()
