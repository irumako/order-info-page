from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field, AliasChoices, field_validator

from .base import Base
from .product import Product


class Order(Base):
    id: str = Field(max_length=16, validation_alias=AliasChoices("id", "Номер"))
    date: datetime = Field(validation_alias=AliasChoices("date", "Дата"))
    contractor: str = Field(max_length=100, validation_alias=AliasChoices("contractor", "Контрагент"))
    amount: Decimal = Field(max_digits=12, decimal_places=2, validation_alias=AliasChoices("amount", "Сумма"))
    files: list[str] = Field(default=[])

    products: List[Product] = Field(validation_alias=AliasChoices("products", "Товары"))

    @field_validator("date", mode="before")
    def parse_order_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(
                value,
                "%Y%m%d"
            ).date()

        return value
