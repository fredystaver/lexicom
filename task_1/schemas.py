import re

from pydantic import BaseModel, constr, validator


class WriteDataRequest(BaseModel):
    phone: constr(min_length=11, max_length=11) = "89502135436"
    address: str

    @validator("phone")
    def validate_number(cls, n: str):
        if not re.fullmatch(r"^\d+$", n):
            raise ValueError('Номер не может содержать в себе не цифру')
        return n


class CheckDataRequest(BaseModel):
    address: str
