from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    access_token = request.cookies.get('booking_access_token')
    if not access_token:
        raise TokenAbsentException
    return access_token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException

    expiration = payload.get('exp')
    if (not expiration) or (int(expiration) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException

    user: Users = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user

