import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.types import Float, TypeDecorator


class PrecisionFloat(TypeDecorator):
    impl = Float

    def __init__(self, precision=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.precision = precision

    def process_bind_param(self, value, dialect):
        if value is not None:
            return round(value, self.precision)


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
