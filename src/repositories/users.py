from typing import Optional
from sqlalchemy import desc
from repositories import BaseRepo
from schemas import UserIn, UserUpdate
from models import User
from sqlalchemy.orm import Session


class UserRepo(BaseRepo[User, UserIn, UserUpdate]):

    def search_by_phone(self, db:Session, phone_in:str) -> Optional[User]:
        return db.query(self.model).filter(self.model.phone == phone_in).first()


    def search_by_email(self, db:Session, email_in:str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email_in).first()


user_repo = UserRepo(User)