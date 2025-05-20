from schemas import ResultIn, UserAuthOut, UserIn, UserOut, UserUpdate
from fastapi import APIRouter, Depends
from api.v1.auth_deps import logged_in
from exceptions import handle_result
from sqlalchemy.orm import Session
from services import users_service
from typing import List, Union
from db import get_db

router = APIRouter()


@router.get('/', response_model=List[Union[ResultIn, List[UserOut]]])
def all_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    all = users_service.get_with_pagination(
        db=db, skip=skip, limit=limit, descending=True, count_results=True)
    return handle_result(all)


@router.post('/', response_model=UserOut)
def create_user(data_in: UserIn, db: Session = Depends(get_db)):
    user = users_service.create_user(db=db, data_in=data_in, flush=False)
    return handle_result(user)


@router.get('/{id}', response_model=UserAuthOut)
def get_one(id, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    todo = users_service.get_one(db, id)
    return handle_result(todo)


@router.put('/{id}', response_model=UserOut)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    update = users_service.update(db, id, data_update=user_update)
    return handle_result(update)
