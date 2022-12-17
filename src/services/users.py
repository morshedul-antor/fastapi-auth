from services import BaseService
from repositories import user_repo
from models import User
from schemas import UserIn, UserUpdate
from sqlalchemy.orm import Session
from exceptions import ServiceResult, AppException
from fastapi import status
from utils import password_hash


class UserService(BaseService[User, UserIn, UserUpdate]):

    def all_user(self, db:Session, skip:int, limit: int):
        all = self.repo.all_user(db=db, skip=skip, limit=limit)

        if not all:
            return ServiceResult([], status_code=status.HTTP_200_OK)
        else: 
            return ServiceResult(all, status_code=status.HTTP_200_OK)
    

    def create_user(self, db:Session, data_in:UserIn, flush:bool):
        # phone & email check
        if self.repo.search_by_phone(db, data_in.phone):
            return ServiceResult(AppException.BadRequest("Phone number already exists!"))
        if self.repo.search_by_email(db, data_in.email):
            return ServiceResult(AppException.BadRequest("Email already exists!"))

        data_obj = data_in.dict(exclude={"password"})
        password = password_hash(data_in.password)
        data_obj.update({"password": password})

        if not flush:
            data = self.repo.create(db, data_in=UserIn(**data_obj))
        else:
            data = self.repo.create_with_flush(db, data_in=UserIn)

        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong!"))
        return ServiceResult(data, status_code=status.HTTP_201_CREATED)



user_service = UserService(User, user_repo)