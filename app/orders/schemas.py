from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from app.orders.models import OrderStatus


class OrderUpdateStatus(BaseModel):
    status: OrderStatus


class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    items: List[OrderItem]


class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: list
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True