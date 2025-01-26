from aiogram import Bot, Dispatcher
from loguru import logger

from src.config import settings
from .middlewares.product_service import ProducrServiceMiddleware
from .handlers.wb_check_products import router


async def start_bot():
    bot = Bot(settings.bot.token)
    dp = Dispatcher()

    dp.update.middleware(ProducrServiceMiddleware())
    dp.include_router(router)

    try:
        logger.info("Bot started")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")
