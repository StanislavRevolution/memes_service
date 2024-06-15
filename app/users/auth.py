from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=90)
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return jwt_token


async def authenticate_user(email: EmailStr, password):
    user: Users = await UsersDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):
        return user

