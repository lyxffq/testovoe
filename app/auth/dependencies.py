from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.users.repository import UsersRepository
from app.exceptions import IncorrectTokenFormatException, UserIsNotPresentException, TokenExpiredException


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise IncorrectTokenFormatException
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except ExpiredSignatureError:
        raise TokenExpiredException    
    except JWTError:
        raise IncorrectTokenFormatException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UsersRepository.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user