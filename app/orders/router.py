from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from app.exceptions import OrderNotFoundException
from app.orders.models import OrderStatus
from app.users.models import Users
from app.orders.dao import OrdersDAO
from app.orders.schemas import OrderCreate, OrderResponse
from app.users.models import Users
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)

@router.post("/")
async def create_order(
    data: OrderCreate,
    user: Users = Depends(get_current_user)
):
    total_price = sum(item.price * item.quantity for item in data.items)

    order = await OrdersDAO.add(
        iser_id=user.id,
        items=[item.dict() for item in data.items],
        total_price=total_price,
        status=OrderStatus.PENDING,
        created_at=datetime.utcnow()
    )

    return order

@router.get("/{order_id}")
async def get_order(
    order_id: str,
    user: Users = Depends(get_current_user)
):
    order = await OrdersDAO.find_one_or_none(id = order_id)

    if not order:
        raise OrderNotFoundException
    
    return order

@router.patch("/{order_id}")
async def update_order(
    order_id: str,
    user: Users = Depends(get_current_user),
):
    order = await OrdersDAO.find_one_or_none(id=order_id)

    if not order:
        raise OrderNotFoundException
    
    update = await OrdersDAO.update(
        {"id": order_id},
        {"status": status}
    )

    return update


@router.get("/user/{user_id}")
async def get_user_orders(
    user_id: int,
    user: Users = Depends(get_current_user)
):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return await OrdersDAO.find_all(user_id=user.id)