from fastapi import APIRouter, Depends, HTTPException, status

from src.depends import get_product_service
from src.scheduler import scheduler
from src.tasks import create_task
from src.schemas import ProductParseInput
from src.services import ProductService

router = APIRouter(prefix="/products")


@router.post("")
async def parse_product(
    product_input: ProductParseInput,
    service: ProductService = Depends(get_product_service),
):
    product = await service.get_product(product_input.articul)
    if product:
        return product

    product = await service.parse_product(product_input.articul)
    if product:
        product_db = await service.save_product(product)
        return product_db

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"product not fount; articul: {product_input.articul}",
    )


@router.get("/subscribe/{artikul}")
async def subscribe_parse_product(
    articul: int,
):
    response = {"is_scheduled": True, "is_new": True, "articul": articul}
    job = scheduler.get_job(str(articul))
    if job is not None:
        response["is_new"] = False
        return response

    await create_task(articul)
    return response
