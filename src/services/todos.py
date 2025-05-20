from exceptions import AppException, ServiceResult
from schemas import TodoIn, TodoUpdate
from repositories import todos_repo
from sqlalchemy.orm import Session
from services import BaseService
from fastapi import status
from models import ToDo


class TodoService(BaseService[ToDo, TodoIn, TodoUpdate]):

    def create_todo(self, db: Session, data_in: TodoIn, user_id: int):
        data_for_db = TodoIn(user_id=user_id, **data_in.dict())
        todo = self.create(db=db, data_in=data_for_db)

        if not todo:
            return ServiceResult(AppException.ServerError("Todo not created!"))
        else:
            return ServiceResult(todo, status_code=status.HTTP_201_CREATED)


todos_service = TodoService(ToDo, todos_repo)
