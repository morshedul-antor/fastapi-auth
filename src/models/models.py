from sqlalchemy import Column, String, Text
from models import BaseModel


class ToDo(BaseModel):
       __tablename__ = "todo"
       title = Column(String(255))
       task = Column(Text, nullable=True)