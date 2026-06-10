from app.repository.base import BaseRepository
from app.orders.models import Orders

class OrdersRepository(BaseRepository):
    model = Orders