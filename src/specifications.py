from typing import Protocol, Type, TypeVar

from sqlalchemy.sql.elements import ColumnElement

from .models import Product


class Specification(Protocol):
    def is_satisfied(self) -> tuple[ColumnElement[bool]]: ...


class FindProductById(Specification):
    def __init__(self, product_id: int):
        self.product_id = product_id

    def is_satisfied(self) -> tuple[ColumnElement[bool]]:
        return (Product.id.__eq__(self.product_id),)

    def __repr__(self) -> str:
        return f"<FindProductById  {self.product_id}>"


class FindProductByArticul(Specification):
    def __init__(self, articul: int):
        self.articul = articul

    def is_satisfied(self) -> tuple[ColumnElement[bool]]:
        return (Product.articul.__eq__(self.articul),)

    def __repr__(self) -> str:
        return f"<FindProductByArticul  {self.articul}>"
