from app.orders.service import OrdersService
from app.orders.domain.status import OrderStatus
from app.orders.utils import calculate_total_price
from app.messaging.producer import publish_new_order

class CreateOrderUseCase:

    def __init__(self, service: OrdersService):
        self.service = service

    async def execute(self, user_id: int, items: list):
        total_price = calculate_total_price(items)

        order = await self.service.create_order(
            user_id=user_id,
            items=[item.dict() for item in items],
            total_price=total_price
        )

        await publish_new_order(order.id)

        return order
    

class UpdateOrderStatusUseCase:

    def __init__(self, service: OrdersService):
        self.service = service

    async def execute(self, order_id: str, status: OrderStatus):
        return await self.service.order_status_update(order_id, status)
