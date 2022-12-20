from pydantic import BaseModel
from typing import Optional
from pydantic.types import constr
from datetime import datetime


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

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    password: str


class UserAuthOut(UserBase):
    created_at: Optional[datetime] = None
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    identifier: str
    password: str


class ResultIn(BaseModel):
    results: int

    class Config:
        orm_mode = True