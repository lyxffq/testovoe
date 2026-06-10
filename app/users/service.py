from app.users.repository import UsersRepository
from app.auth.password_service import hash_password, verify_password


class UsersService:

    async def register(self, email: str, password: str):
        existing_user = await UsersRepository.find_one_or_none(email=email)

        if existing_user:
            return None
        
        hashed = hash_password(password)

        return await UsersRepository.add(
            email=email,
            hashed_password = hashed 
        )
    
    async def authenticate(self, email: str, password: str):
        user = await UsersRepository.find_one_or_none(email=email)

        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user