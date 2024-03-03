from decimal import Decimal

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(max_length=250, validation_alias="Наименование")
    quantity: int = Field(gt=0, validation_alias="Количество")
    unit: str = Field(max_length=10, validation_alias="Единица")
    price: Decimal = Field(max_digits=6, decimal_places=2, validation_alias="Цена")
    amount: Decimal = Field(max_digits=6, decimal_places=2, validation_alias="Сумма")
