from fastapi import APIRouter, Depends
from schemas import UserLogin, UserAuthOut, Token
from exceptions import handle_result
from sqlalchemy.orm import Session
from db import get_db
from services import user_service
from models import User
from api.v1.auth_deps import logged_in

router = APIRouter()

@router.post('/login/', response_model=Token)
def login(data_in: UserLogin, db: Session = Depends(get_db)):
    user = user_service.login(db, data_in.identifier, data_in.password)
    return handle_result(user)


@router.get('/auth/', response_model=UserAuthOut)
def auth(current_user: User = Depends(logged_in)):
    return current_user