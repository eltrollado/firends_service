import aioredis

from app.config import settings


class RedisCache:
    redis: aioredis.Redis = None

    async def connect(self):
        self.redis = await aioredis.create_redis_pool(f'redis://{settings.redis_url}')

    async def disconnect(self):
        pass

    async def cached_set(self, key, task, mapper):
        assert key
        cached = await self.redis.smembers(key)

        if cached:
            return list(map(mapper, cached))

        data = await task

        if data:
            await self.redis.sadd(key, *data)
            return data
        else:
            return []

    async def delete(self, key):
        await self.redis.delete(key)


cache = RedisCache()
