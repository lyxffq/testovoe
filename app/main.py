from fastapi import FastAPI

from app.users.models import Users
from app.orders.models import Orders
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)