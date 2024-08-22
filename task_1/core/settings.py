from functools import lru_cache

import yaml
from pydantic_settings import BaseSettings

from task_1.core.constants import SETTINGS_PATH


class ApiSettings(BaseSettings):
    title: str
    host: str
    port: int


class RedisSettings(BaseSettings):
    host: str
    port: int


class Settings(BaseSettings):
    api: ApiSettings
    redis: RedisSettings


@lru_cache
def get_settings() -> Settings:
    with open(SETTINGS_PATH) as file:
        settings = Settings.model_validate(yaml.load(file, Loader=yaml.FullLoader))

    return settings
