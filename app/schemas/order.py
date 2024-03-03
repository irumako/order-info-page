from datetime import datetime, date
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, field_validator

from product import Product


class Order(BaseModel):
    id: str = Field(max_length=16, validation_alias="Номер")
    created_at: date = Field(validation_alias="Дата", serialization_alias="date")
    contractor: str = Field(max_length=100, validation_alias="Контрагент")
    amount: Decimal = Field(max_digits=12, decimal_places=2, validation_alias="Сумма")

    products: List[Product] = Field(alias="Товары")

    @field_validator("created_at", mode="before")
    def parse_order_date(cls, value):
        return datetime.strptime(
            value,
            "%Y%m%d"
        ).date()

