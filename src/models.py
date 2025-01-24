from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    func,
    BigInteger,
    DECIMAL,
    SmallInteger,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseDBModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class Product(BaseDBModel):
    __tablename__ = "products"

    articul: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)
    title: Mapped[str] = mapped_column(String)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=12, scale=2))
    quantity_sum: Mapped[int] = mapped_column(Integer)
    rating: Mapped[int] = mapped_column(SmallInteger)
