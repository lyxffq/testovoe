from app.repository.base import BaseRepository
from app.users.models import Users


class UsersRepository(BaseRepository):
    model = Users