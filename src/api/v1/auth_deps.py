from fastapi import Depends
from db import get_db
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from sqlalchemy.orm import Session
from exceptions.app_exceptions import AppException
from exceptions.service_result import handle_result
from services import user_service
from utils import Token

security = HTTPBearer()


def logged_in(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    token_data = Token.validate_token(token)
    user = handle_result(user_service.get_one(db, id=token_data.user_id))

    if not user:
        raise AppException.Unauthorized()
    return user