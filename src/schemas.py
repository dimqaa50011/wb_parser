from decimal import Decimal
from typing import Optional, Self
from pydantic import BaseModel, field_validator, model_validator


class ProductCreate(BaseModel):
    aricul: int
    title: str
    price: Decimal
    rating: float
    quantity_sum: int

    @field_validator("rating", mode="before")
    def check_max_value_rating(cls, v: float):
        if v > 5.0:
            raise ValueError("Value must not exceed 5.0")
        return v


class ProductRead(ProductCreate):
    id: int


class ProductRefresh(BaseModel):
    aricul: Optional[int] = None
    title: Optional[str] = None
    price: Optional[Decimal] = None
    rating: Optional[float] = None
    quantity_sum: Optional[int] = None

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> Self:
        if not any(
            getattr(self, field) is not None
            for field in [field for field in self.model_fields.keys()]
        ):
            raise ValueError("At least one field must be set")
        return self
