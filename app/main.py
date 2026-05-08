from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.config import settings
from app.users.models import Users
from app.orders.models import Orders

from app.users.router import router as router_users
from app.orders.router import router as router_orders


@asynccontextmanager
async def lifespan(app):
    redis = await aioredis.from_url(settings.REDIS_DB_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()



app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_orders)


origins = [
    "http://localhost:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow_origin", "Authorization"],
)

