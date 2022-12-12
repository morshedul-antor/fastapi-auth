from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
       title: str
       task: Optional[str] = None


class TodoIn(TodoBase):
       pass


class TodoOut(TodoBase):
       id: int

       class Config:
              orm_mode = True


class TodoUpdate(BaseModel):
       title: str
       task: Optional[str] = None
