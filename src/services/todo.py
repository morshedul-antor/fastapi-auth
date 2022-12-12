from services import BaseService
from repositories import todo_repo
from models import ToDo
from schemas import TodoBase, TodoIn, TodoUpdate
from sqlalchemy.orm import Session
from exceptions import ServiceResult, AppException
from fastapi import status

class TodoService(BaseService[ToDo, TodoIn, TodoUpdate]):

    def all_todo(self, db:Session, skip: int, limit: int):
        all = self.repo.all_todo(db=db, skip=skip, limit=limit)
        
        if not all:
            return ServiceResult([], status_code=status.HTTP_200_OK)
        else:
            return ServiceResult(all, status_code=status.HTTP_200_OK)


    def create_todo(self, db: Session, data_in: TodoBase):
        todo = self.repo.create_todo(db=db, data_in=data_in)

        if not todo:
            return ServiceResult(AppException.ServerError("Todo not created!"))
        else:
            return ServiceResult(todo, status_code=status.HTTP_201_CREATED)



todo_service = TodoService(ToDo, todo_repo)