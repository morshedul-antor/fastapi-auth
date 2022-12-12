from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
from fastapi import status
from db import Base
from pydantic import BaseModel
from repositories import BaseRepo
from exceptions import AppException, ServiceResult


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelRepo = TypeVar("ModelRepo", bound=BaseRepo)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], repo: Type[ModelRepo]):
        self.model = model
        self.repo = repo

    def create(self, db: Session, data_in: CreateSchemaType):
        data = self.repo.create(db, data_in)
        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong!"))
        return ServiceResult(data, status_code=status.HTTP_201_CREATED)

    def create_with_flush(self, db: Session, data_in: CreateSchemaType):
        data = self.repo.create_with_flush(db, data_in)
        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong!"))
        return ServiceResult(data, status_code=status.HTTP_201_CREATED)

    def get(self, db: Session):
        data = self.repo.get(db)
        if not data:
            data = []
            # return ServiceResult(AppException.NotFound(f"No {self.model.__name__.lower}s found."))
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_one(self, db: Session, id: int):
        data = self.repo.get_one(db, id)
        if not data:
            return ServiceResult(AppException.NotFound(f"No {self.model.__name__.lower}s found."))
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_with_pagination(self, db: Session, skip: int, limit: int, descending: bool = False, count_results: bool = False):
        data = self.repo.get_with_pagination(
            db=db, skip=skip, limit=limit, descending=descending, count_results=count_results)

        if not data:
            if count_results is True:
                data = [{"results": 0}, []]
            else:
                data = []
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_by_key_first(self, db: Session, **kwargs):
        data = self.repo.get_by_key_first(db=db, **kwargs)
        if not data:
            return ServiceResult(AppException.ServerError("Data not found!"))
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_by_key(self, db: Session, skip: int, limit: int, descending: bool, count_results: bool, **kwargs):
        data = self.repo.get_by_key(
            db=db, skip=skip, limit=limit, descending=descending, count_results=count_results, **kwargs)

        if not data:
            data = []
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_by_two_key(self, db: Session, skip: int, limit: int, descending: bool, count_results: bool, **kwargs):
        data = self.repo.get_by_two_key(
            db=db, skip=skip, limit=limit, descending=descending, count_results=count_results, **kwargs)

        if not data:
            data = []
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def update(self, db: Session, id: int, data_update: UpdateSchemaType):
        data = self.repo.update(db, id, data_update)
        if not data:
            return ServiceResult(AppException.NotAccepted())
        return ServiceResult(data, status_code=status.HTTP_202_ACCEPTED)

    def update_before_check(self, db: Session, id: int, data_update: UpdateSchemaType, **kwargs):
        get_data = self.repo.get_by_two_key(db=db, skip=0, limit=10, descending=False, count_results=False, id=id, **kwargs)
        if not get_data:
            return ServiceResult(AppException.ServerError("Access denied"))
        return self.update(db=db, id=id, data_update=data_update)

    def delete(self, db: Session, id: int):
        remove = self.repo.delete(db, id)
        if remove:
            return ServiceResult("Deleted", status_code=status.HTTP_202_ACCEPTED)
        return ServiceResult(AppException.Forbidden())
