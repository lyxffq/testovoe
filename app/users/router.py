from fastapi import APIRouter, Depends, Response

from app.users.schemas import UserLogin, UserRegister
from app.users.service import UsersService
from app.users.use_cases import RegisterUserUseCase, LoginUserUseCase
from app.exceptions import UserAlreadyExistException, UserIsNotPresentException

router = APIRouter(
    prefix="",
    tags=["Авторизация"]
)

service = UsersService()

@router.post("/register")
async def register_user(data: UserRegister):
    use_case = RegisterUserUseCase(service)

    result = await use_case.execute(data.email, data.password)

    if not result:
        raise UserAlreadyExistException
    
    return "Успешная регистрация"


@router.post("/login")
async def login_user(data: UserLogin, response: Response):
    use_case = LoginUserUseCase(service)

    token = await use_case.execute(data.email, data.password)

    if not token:
        raise UserIsNotPresentException
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return token