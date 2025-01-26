from decimal import Decimal

from fastapi import HTTPException, status

from .auth import create_password_hash, verify_password

from .errors import ProductNotCreated
from .schemas import (
    AdminSchema,
    FormattedData,
    ParsedData,
    ProductCreate,
    ProductRead,
    ProductRefresh,
)
from .specifications import FindAdminByUsername, FindProductByArticul
from .clients.wildberries import WildberiesParser
from .models import Admin, Product
from .repositories import BaseRepositoryProtocol


class ProductService:
    def __init__(
        self,
        product_repository: BaseRepositoryProtocol[Product],
        parser: WildberiesParser,
    ) -> None:
        self._product_repo = product_repository
        self._parser = parser

    async def get_product(self, articul: int):
        product = await self._product_repo.find(FindProductByArticul(articul))
        if product is not None:
            return ProductRead.model_validate(product, from_attributes=True)

    async def parse_product(self, articul: int):
        parsed_product = await self._parser.get_product(articul)
        if parsed_product is None:
            return

        parsed_product_data = ParsedData.model_validate(
            parsed_product["data"], from_attributes=True
        )

        return FormattedData.model_validate(
            parsed_product_data.products[0], from_attributes=True
        )

    async def save_product(self, data: FormattedData) -> ProductRead:
        product = await self._product_repo.create(
            ProductCreate(
                articul=data.articul,
                title=data.title,
                price=Decimal(data.price),
                sale_price=Decimal(data.sale_price) if data.sale_price else None,
                rating=data.rating,
                quantity_sum=data.quantity_sum,
            ).model_dump()
        )
        return ProductRead.model_validate(product, from_attributes=True)

    async def update_product(self, articul: int, data: ProductRefresh):
        await self._product_repo.refresh(
            FindProductByArticul(articul), data.model_dump(exclude_none=True)
        )


class AdminService:
    def __init__(self, admin_repository: BaseRepositoryProtocol[Admin]) -> None:
        self._admin_repo = admin_repository

    async def get_admin(self, username: str, password: str):
        admin = await self._admin_repo.find(FindAdminByUsername(username))
        return admin

    async def verify_admin(self, password: str, hashed_password: str) -> bool:
        return verify_password(password, hashed_password)

    async def create_admin(self, admin: AdminSchema) -> str:
        hashed_password = create_password_hash(admin.password)
        new_admin = await self._admin_repo.create(
            {"username": admin.username, "password_hash": hashed_password}
        )
        return new_admin.username
