from fastapi import HTTPException, status

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже существует'
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверная почта или пароль'
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек'
)

TokenAbsentException=HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен отсутствует'
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверный формат токена'
)

UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не существует пользователя"
)

OrderNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Не найден заказ"
)

