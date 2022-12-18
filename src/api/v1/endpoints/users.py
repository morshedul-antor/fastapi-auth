from fastapi import APIRouter, Depends
from schemas import UserIn, UserOut, UserUpdate
from exceptions import handle_result
from sqlalchemy.orm import Session
from db import get_db
from typing import List
from services import user_service

router = APIRouter()

@router.get('/', response_model=List[UserOut])
def all_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    all = user_service.get_with_pagination(db=db, skip=skip, limit=limit)
    return handle_result(all)


@router.post('/', response_model=UserOut)
def create_user(data_in: UserIn, db: Session = Depends(get_db)):
    user = user_service.create_user(db=db, data_in=data_in, flush=False)
    return handle_result(user)


@router.get('/{id}', response_model=UserOut)
def get_one(id, db: Session = Depends(get_db)):
    todo = user_service.get_one(db, id)
    return handle_result(todo)


@router.put('/{id}', response_model=UserOut)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    update = user_service.update(db, id, data_update=user_update)
    return handle_result(update)