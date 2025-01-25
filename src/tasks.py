from datetime import datetime

from .config import settings
from .db_session import Session
from .schemas import ProductRefresh
from .depends import get_product_service
from .scheduler import scheduler


async def create_task(articul: int):

    scheduler.add_job(
        interval_parse,
        trigger="interval",
        minutes=settings.scheduler.interval_minutes,
        args=(articul,),
        id=str(articul),
        misfire_grace_time=30,
        next_run_time=datetime.now(),
    )


async def interval_parse(articul: int):
    async with Session() as sess:
        service = await get_product_service(sess)
        product = await service.parse_product(articul)
        if product:
            product_db = await service.get_product(articul)
            if product_db is None:
                await service.save_product(product)
                return
            await service.update_product(
                articul,
                ProductRefresh(
                    title=product.title,
                    rating=product.rating,
                    quantity_sum=product.quantity_sum,
                    price=product.price,
                ),
            )
