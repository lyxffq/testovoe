import enum
import uuid
from sqlalchemy import String, JSON, Column, DateTime, Float, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"

class Orders(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(ForeignKey("users.id"))
    items = Column(JSON, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="orders")