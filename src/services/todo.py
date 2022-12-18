from services import BaseService
from repositories import todo_repo
from models import ToDo
from schemas import TodoIn, TodoUpdate
from sqlalchemy.orm import Session
from exceptions import ServiceResult, AppException
from fastapi import status


class TodoService(BaseService[ToDo, TodoIn, TodoUpdate]):

    def create_todo(self, db:Session, data_in:TodoIn, user_id:int):
        todo = self.repo.create_todo(db=db, data_in=data_in, user_id=user_id)

        if not todo:
            return ServiceResult(AppException.ServerError("Todo not created!"))
        else:
            return ServiceResult(todo, status_code=status.HTTP_201_CREATED)



todo_service = TodoService(ToDo, todo_repo)