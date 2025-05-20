from fastapi import status
from sqlalchemy.orm import Session

from exceptions import AppException, ServiceResult
from models import ToDo
from repositories import todo_repo
from schemas import TodoIn, TodoUpdate
from services import BaseService


class TodoService(BaseService[ToDo, TodoIn, TodoUpdate]):

    def create_todo(self, db: Session, data_in: TodoIn, user_id: int):
        data_for_db = TodoIn(user_id=user_id, **data_in.dict())
        todo = self.create(db=db, data_in=data_for_db)

        if not todo:
            return ServiceResult(AppException.ServerError("Todo not created!"))
        else:
            return ServiceResult(todo, status_code=status.HTTP_201_CREATED)


todo_service = TodoService(ToDo, todo_repo)
