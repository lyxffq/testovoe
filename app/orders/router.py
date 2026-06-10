
from fastapi import APIRouter, Depends, HTTPException


from app.exceptions import OrderNotFoundException
from app.orders.schemas import OrderCreate, OrderUpdateStatus
from app.auth.dependencies import get_current_user
from app.orders.service import OrdersService
from app.orders.use_cases import UpdateOrderStatusUseCase, CreateOrderUseCase

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)

service = OrdersService()

@router.post("/")
async def create_order(
    data: OrderCreate,
    user=Depends(get_current_user),
):
    use_case = CreateOrderUseCase(service)

    return await use_case.execute(
        user.id,
        data.items
    )

@router.patch("/{order_id}")
async def update_order_status(order_id: str, data: OrderUpdateStatus):
    use_case = UpdateOrderStatusUseCase(service)

    return await use_case.execute(order_id, data.status)

@router.get("/{order_id}")
async def get_order(order_id: str):
    return await service.get_order(order_id)

@router.get("/user/{user_id}")
async def get_user_orders(user_id: int, user=Depends(get_current_user)):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return await service.get_user_orders(user_id)