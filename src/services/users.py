from services import BaseService
from repositories import user_repo
from models import User
from schemas import UserIn, UserUpdate
from sqlalchemy.orm import Session
from exceptions import ServiceResult, AppException
from fastapi import status
from utils import password_hash, verify_password, Token


class UserService(BaseService[User, UserIn, UserUpdate]):

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


    def is_auth(self, db: Session, identifier: str, password: str):
        user_by_email = self.repo.search_by_email(db, email_in=identifier)
        user_by_phone = self.repo.search_by_phone(db, phone_in=identifier)

        if user_by_email and verify_password(password, user_by_email.password):
            return user_by_email
        elif user_by_phone and verify_password(password, user_by_phone.password):
            return user_by_phone
        else:
            return None


    def login(self, db: Session, identifier: str, password: str):
        user: User = self.is_auth(db, identifier, password)

        # deactive user prevent
        # if user and user.is_active == False:
        #     return ServiceResult(AppException.NotFound("You are not active user."))

        if user is not None:          
            # access token
            access_token = Token.create_access_token({"sub": user.id})
            return ServiceResult({"access_token": access_token, "token_type": "bearer"}, status_code=200)
        else:
            return ServiceResult(AppException.NotFound("User not found"))



user_service = UserService(User, user_repo)