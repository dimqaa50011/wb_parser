from fastapi import APIRouter, Depends

from src.depends import get_admin_service, login_user
from src.services import AdminService
from src.schemas import AdminSchema, Token

router = APIRouter(prefix="/auth")


@router.post("/register")
async def create_new_admin(
    admin: AdminSchema, service: AdminService = Depends(get_admin_service)
):
    username = await service.create_admin(admin)
    return {"username": username}


@router.post("/login")
async def login_admin(token: Token = Depends(login_user)):
    return token
