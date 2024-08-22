from fastapi import HTTPException, status


class BaseExceptions(HTTPException):
    status_code: int = ...
    detail: str = ...

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFoundException(BaseExceptions):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Номер не найден'
