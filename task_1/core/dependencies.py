from typing import Type, TypeVar, Callable, Awaitable

from fastapi import Depends
from redis.asyncio import Redis
from starlette.requests import Request

from task_1.core.controller import BaseController
from task_1.core.settings import Settings, get_settings

Controller = TypeVar("Controller", bound=BaseController)


async def get_radis_connection(
    request: Request,
):
    async with request.app.state.redis as redis_:
        yield redis_


def get_controller(
    controller_class: Type[Controller]
) -> Callable[[], Awaitable[Controller]]:
    async def _get_controller(
        settings: Settings = Depends(get_settings),
        redis: Redis = Depends(get_radis_connection)
    ) -> Controller:
        return controller_class(
            settings=settings,
            redis=redis,
        )

    return _get_controller
