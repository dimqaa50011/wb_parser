from fastapi import APIRouter

from .products import router as products_router

router = APIRouter(prefix="/api/v1")

router.include_router(products_router)
