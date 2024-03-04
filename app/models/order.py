import datetime
from typing import List

from sqlalchemy import String, Float, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Order(Base):

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    contractor: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(Float(2), nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="order")
