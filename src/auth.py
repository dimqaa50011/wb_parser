from fastapi import Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
import bcrypt

from .config import settings


access_security = JwtAccessBearer(secret_key=settings.auth.salt)


def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return credentials.subject


def create_password_hash(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
