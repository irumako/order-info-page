import datetime
from typing import List

from sqlalchemy import String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, PrecisionFloat


class Order(Base):

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    contractor: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(PrecisionFloat(2), nullable=False)
    files: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)

    products: Mapped[List["Product"]] = relationship(back_populates="order", lazy="selectin")
