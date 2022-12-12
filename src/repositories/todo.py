from sqlalchemy import desc
from repositories import BaseRepo
from schemas import TodoBase, TodoIn, TodoUpdate 
from models import ToDo
from sqlalchemy.orm import Session

from schemas.todo import TodoBase


class TodoRepo(BaseRepo[ToDo, TodoIn, TodoUpdate]):

    def all_todo(self, db:Session, skip: int, limit: int):
        query = db.query(self.model).order_by(desc(self.model.created_at)).offset(skip).limit(limit).all()
        return query

    def create_todo(self, db: Session, data_in:TodoBase):
        data_for_db = TodoIn(**data_in.dict())
        todo = self.create(db=db, data_in=data_for_db)
        return todo


todo_repo = TodoRepo(ToDo)