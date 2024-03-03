import uuid

from sqlalchemy import String, UUID, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Product(Base):

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    quantity: Mapped[int] = mapped_column(String(3), nullable=False)
    unit: Mapped[str] = mapped_column(String(10))
    price: Mapped[float] = mapped_column(Float(2), nullable=False)
    amount: Mapped[float] = mapped_column(Float(2), nullable=False)

    order_id: Mapped[str] = mapped_column(ForeignKey("order.id"))
    order: Mapped["Order"] = relationship(back_populates="products")
