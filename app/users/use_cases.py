from app.users.service import UsersService
from app.auth.jwt_service import create_access_token

class RegisterUserUseCase:
    def __init__(self, service: UsersService):
        self.service = service

    async def execute(self, email: str, password: str):
        return await self.service.register(email, password)    
    
class LoginUserUseCase:
    def __init__(self, service: UsersService):
        self.service = service

    async def execute(self, email: str, password: str):
        user = await self.service.authenticate(email, password)

        if not user:
            return None
        
        return create_access_token(
            {"sub": str(user.id)}
        )