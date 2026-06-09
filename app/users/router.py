from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth import create_access_token, hash_password, verify_password
from app.users.dao import UsersDAO
from app.users.schemas import UserLogin, UserRegister
from app.exceptions import IncorrectTokenFormatException, UserAlreadyExistException, UserIsNotPresentException

router = APIRouter(
    prefix="",
    tags=["Авторизация"]
)

@router.post("/register/")
async def register_user(user_data: UserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistException
    
    hashed_password = hash_password(user_data.password)

    user = await UsersDAO.add(
        email=user_data.email,
        hashed_password=hashed_password
    )

    return "Пользователь зарегистрирован"


@router.post("/token/")
async def login_user(
    response: Response,
    data: UserLogin
):
    user = await UsersDAO.find_one_or_none(email=data.email)

    if not user:
        raise UserIsNotPresentException

    if not verify_password(data.password, user.hashed_password):
        raise IncorrectTokenFormatException

    access_token = create_access_token({
        "sub": str(user.id)
    })

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
    )