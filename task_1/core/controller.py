from abc import ABC

from pydantic_settings import BaseSettings
from redis.asyncio import Redis


class BaseController(ABC):

    def __init__(
        self,
        redis: Redis,
        settings: BaseSettings = None,
    ) -> None:
        self._settings = settings
        self._redis = redis
