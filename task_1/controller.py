from task_1.core.controller import BaseController
from task_1.core.exceptions import NotFoundException
from task_1.schemas import CheckDataRequest


class AppController(BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def write_data(self, phone: str, address: str) -> None:
        await self._redis.set(phone, address)

    async def check_data(self, phone: str) -> CheckDataRequest:
        if data := await self._redis.get(name=phone):
            return data
        raise NotFoundException
