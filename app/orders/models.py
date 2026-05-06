import enum
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship

from app.database import Base

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELED = "cancelled"

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    items = Column(JSON, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="order")