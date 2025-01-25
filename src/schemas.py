from decimal import Decimal
from typing import Optional, Self
from pydantic import BaseModel, Field, field_validator, model_validator


class ProductCreate(BaseModel):
    articul: int
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


class StokData(BaseModel):
    qty: int


class SizeData(BaseModel):
    stocks: list[StokData]


class ParsedProducts(BaseModel):
    articul: int = Field(default=..., alias="id")
    title: str = Field(default=..., alias="name")
    rating: float = Field(default=..., alias="reviewRating")
    price: int = Field(default=..., alias="priceU")
    sizes: list[SizeData]


class ParsedData(BaseModel):
    products: list[ParsedProducts]


class FormattedData(BaseModel):
    articul: int
    title: str
    rating: float
    price: int
    quantity_sum: int = 0

    sizes: list[SizeData]

    @model_validator(mode="after")
    def compute_quamtity_summ(self):
        control_summ = 0
        for size in self.sizes:
            for stock in size.stocks:
                control_summ += stock.qty

        self.quantity_sum = control_summ
        return self
