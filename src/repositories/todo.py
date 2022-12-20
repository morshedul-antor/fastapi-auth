from repositories import BaseRepo
from schemas import TodoIn, TodoUpdate 
from models import ToDo
from sqlalchemy.orm import Session


class TodoRepo(BaseRepo[ToDo, TodoIn, TodoUpdate]):

    def create_todo(self, db:Session, data_in:TodoIn, user_id:int):
        data_for_db = TodoIn(user_id=user_id, **data_in.dict())
        todo = self.create(db=db, data_in=data_for_db)
        return todo


todo_repo = TodoRepo(ToDo)