from fastapi import APIRouter, Depends

from task_1.controller import AppController
from task_1.core.dependencies import get_controller
from task_1.schemas import WriteDataRequest, CheckDataRequest

router = APIRouter(
    tags=["data"]
)


@router.get("/check_data")
async def check_data(
    phone: str,
    controller: AppController = Depends(get_controller(AppController))
) -> CheckDataRequest:
    return await controller.check_data(phone=phone)


@router.post("/write_data")
async def write_data(
    body: WriteDataRequest,
    controller: AppController = Depends(get_controller(AppController)),
) -> None:
    return await controller.write_data(phone=body.phone, address=body.address)


@router.put("/write_data")
async def write_data(
    body: WriteDataRequest,
    controller: AppController = Depends(get_controller(AppController)),
) -> None:
    return await controller.write_data(phone=body.phone, address=body.address)
