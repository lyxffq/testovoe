from app.orders.repository import OrdersRepository
from app.orders.domain.status import OrderStatus
from app.orders.integrations.rediscache import RedisCache
from app.orders.utils import order_to_dict

class OrdersService:

    def __init__(self):
        self.cache = RedisCache()

    async def create_order(
            self,
            user_id: int,
            items: list,
            total_price: float
        ):
        return await OrdersRepository.add(
            user_id=user_id,
            items=items,
            total_price=total_price,
            status=OrderStatus.PENDING
        )
    

    async def get_order(self, order_id: str):
        cache_key = f"order:{order_id}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        order = await OrdersRepository.find_one_or_none(id=order_id)

        if not order:
            return None
        
        result = order_to_dict(order)

        await self.cache.set(cache_key, result)

        return result

    async def get_user_orders(self, user_id: int):
        return await OrdersRepository.find_all(user_id=user_id)
    

    async def order_status_update(self, order_id: str, status: OrderStatus):
        order = await OrdersRepository.find_one_or_none(id=order_id)

        if not order:
            return None
        
        updated = await OrdersRepository.update(
            {"id": order_id},
            {"status": status.value if hasattr(status, "value") else status}
        )

        await self.cache.delete(f"order:{order_id}")

        return updated