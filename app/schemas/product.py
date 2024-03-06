from decimal import Decimal

from pydantic import AliasChoices, Field

import models
from .base import Base


class Product(Base):
    name: str = Field(max_length=250, validation_alias=AliasChoices("name", "Наименование"))
    quantity: int = Field(gt=0, validation_alias=AliasChoices("quantity", "Количество"))
    unit: str = Field(max_length=10, validation_alias=AliasChoices("unit", "Единица"))
    price: Decimal = Field(max_digits=12, decimal_places=2, validation_alias=AliasChoices("price", "Цена"))
    amount: Decimal = Field(max_digits=12, decimal_places=2, validation_alias=AliasChoices("amount", "Сумма"))

    class Meta:
        orm_model = models.Product
