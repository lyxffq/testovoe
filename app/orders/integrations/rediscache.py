import json
from redis import asyncio as aioredis

from app.config import settings

class RedisCache:
    def __init__(self):
        self.redis = aioredis.from_url(
            settings.REDIS_DB_URL,
            encoding="utf-8",
        )

    async def get(self, key: str):
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        else:
            return None
        
    async def set(self, key: str, value: dict, ttl: int = 300):
        await self.redis.set(
            key,
            json.dumps(value),
            ex=ttl
        )

    async def delete(self, key: str):
        await self.redis.delete(key)