from fastapi.security import HTTPBasicCredentials, HTTPBearer
from exceptions import AppException, handle_result
from sqlalchemy.orm import Session
from services import users_service
from fastapi import Depends
from utils import Token
from db import get_db

security = HTTPBearer()


def logged_in(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    token_data = Token.validate_token(token)
    user = handle_result(users_service.get_one(db, id=token_data.user_id))

    if not user:
        raise AppException.Unauthorized()
    return user
