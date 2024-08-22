from typing import Callable, Awaitable

from fastapi import FastAPI
from redis import asyncio as aioredis
from task_1.core.settings import RedisSettings


def setup_redis_connection(app: FastAPI, settings: RedisSettings) -> Callable[[], Awaitable[None]]:
    async def redis() -> None:
        redis_ = aioredis.from_url(
            url=f"redis://{settings.host}:{settings.port}",
            encoding="utf-8",
            decode_responses=True,
        )
        app.state.redis = redis_

    return redis


def close_redis_connection(app: FastAPI) -> Callable[[], Awaitable[None]]:
    async def redis() -> None:
        await app.state.redis.flushall()
        await app.state.redis.close()

    return redis
