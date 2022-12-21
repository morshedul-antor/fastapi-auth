from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from models import BaseModel


#==============#
# User Related #
#==============#
class User(BaseModel):
       __tablename__ = "users"
       name = Column(String(100), nullable=False)
       phone = Column(String(20), nullable=False)
       email = Column(String(30), nullable=True)
       password = Column(String(255), nullable=False)
       log_info = Column(DateTime(timezone=True), default=func.now())


#==============#
# Todo Related #
#==============#
class ToDo(BaseModel):
       __tablename__ = "todo"
       title = Column(String(255))
       task = Column(Text, nullable=True)
       user_id = Column(Integer, ForeignKey("users.id"))