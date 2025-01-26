from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.db_session import Session
from src.services import ProductService
from src.repositories import ProductRepository
from src.clients.wildberries import WildberiesParser


class ProducrServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with Session() as session:
            data["service"] = ProductService(
                product_repository=ProductRepository(session), parser=WildberiesParser()
            )
            await handler(event, data)
