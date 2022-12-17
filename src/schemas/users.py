from pydantic import BaseModel
from typing import Optional
from pydantic.types import constr


class UserBase(BaseModel):
    name: str
    phone: constr(
        min_length=11, max_length=14, regex=r"(^(\+88)?(01){1}[3-9]{1}\d{8})$"
    )
    email: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    name: str
    phone: str
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    password: str