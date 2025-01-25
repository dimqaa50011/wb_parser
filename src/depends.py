from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .clients.wildberries import WildberiesParser
from .repositories import ProductRepository
from .services import ProductService
from .db_session import Session


async def get_session():
    async with Session() as session:
        yield session


async def get_product_service(session: AsyncSession = Depends(get_session)):
    return ProductService(
        product_repository=ProductRepository(session), parser=WildberiesParser()
    )
