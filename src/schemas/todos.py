from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    title: str
    task: Optional[str] = None


class TodoIn(TodoBase):
    user_id: Optional[int] = None


class TodoOut(TodoBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True


class TodoOutUser(TodoBase):
    id: int

    class Config:
        orm_mode = True


class TodoUpdate(BaseModel):
    title: str
    task: Optional[str] = None
