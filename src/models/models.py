import email
from sqlalchemy import Column, String, Text
from models import BaseModel


class ToDo(BaseModel):
       __tablename__ = "todo"
       title = Column(String(255))
       task = Column(Text, nullable=True)


class User(BaseModel):
       __tablename__ = "users"
       name = Column(String(100), nullable=False)
       phone = Column(String(20), nullable=False)
       email = Column(String(30), nullable=True)
       password = Column(String(255), nullable=False)