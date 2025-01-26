from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from .schemas import AdminSchema, Token

from .clients.wildberries import WildberiesParser
from .repositories import AdminRepository, ProductRepository
from .services import AdminService, ProductService
from .db_session import Session
from .auth import access_security, get_current_user, verify_password


async def get_session():
    async with Session() as session:
        yield session


async def get_product_service(session: AsyncSession = Depends(get_session)):
    return ProductService(
        product_repository=ProductRepository(session), parser=WildberiesParser()
    )


async def get_admin_service(session: AsyncSession = Depends(get_session)):
    return AdminService(admin_repository=AdminRepository(session))


async def login_user(
    admin: AdminSchema, service: AdminService = Depends(get_admin_service)
) -> Token:
    ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_in_db = await service.get_admin(admin.username, admin.password)
    if user_in_db is None:
        raise ex
    if not service.verify_admin(admin.password, user_in_db.password_hash):
        raise ex
    return Token(
        token_type="Bearer",
        access_token=access_security.create_access_token(
            subject={"username": user_in_db.username, "id": user_in_db.id}
        ),
    )


def login_required(admin: AdminSchema = Depends(get_current_user)) -> AdminSchema:
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return admin
