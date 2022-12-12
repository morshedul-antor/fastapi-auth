from typing import Any, Generic, Optional, Type, TypeVar, List, Union
from sqlalchemy import desc
from sqlalchemy.orm import Session
from db import Base
from models import BaseModel
from repositories.base_abstract import ABSRepo

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepo(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABSRepo):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    """"Data create related methods"""

    def create(self, db: Session, data_in: CreateSchemaType) -> ModelType:
        data = self.model(**data_in.dict())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    def create_with_flush(self, db: Session, data_in: CreateSchemaType):
        data = self.model(**data_in.dict())
        db.add(data)
        db.flush()
        return data

    def create_commit_after_flush(self, db: Session, data_obj: ModelType):
        db.commit()
        db.refresh(data_obj)
        return data_obj

    """Data get related methods"""

    def get(self, db: Session) -> List[ModelType]:
        query = db.query(self.model).all()
        return query

    def get_one(self, db: Session, id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_with_pagination(self, db: Session, skip: int, limit: int, descending: bool = False, count_results: bool = False):

        query = db.query(self.model).all()

        if descending == True:
            data = db.query(self.model).order_by(
                desc(self.model.created_at)).offset(skip).limit(limit).all()
        else:
            data = db.query(self.model).offset(skip).limit(limit).all()

        if count_results == True:
            return [{"results": len(query)}, data]
        return data

    def get_by_key_first(self, db: Session, **kwargs):
        search_key = list(kwargs.items())[0][0]
        search_value = list(kwargs.items())[0][1]

        query = db.query(self.model).filter(getattr(self.model, search_key) == search_value).first()
        return query

    def get_by_key(self, db: Session, skip: int, limit: int, descending: bool = False, count_results: bool = False, **kwargs):
        search_key = list(kwargs.items())[0][0]
        search_value = list(kwargs.items())[0][1]

        query = db.query(self.model).filter(
            getattr(self.model, search_key) == search_value).all()

        if descending == True:
            data = db.query(self.model).filter(getattr(self.model, search_key) == search_value).order_by(
                desc(self.model.created_at)).offset(skip).limit(limit).all()
        else:
            data = db.query(self.model).filter(
                getattr(self.model, search_key) == search_value).offset(skip).limit(limit).all()

        if count_results == True:
            return [{"results": len(query)}, data]
        return data

    def get_by_two_key(self, db: Session, skip: int, limit: int, descending: bool = False, count_results: bool = False, **kwargs):
        search_key = list(kwargs.items())[0][0]
        search_value = list(kwargs.items())[0][1]

        second_search_key = list(kwargs.items())[1][0]
        second_search_value = list(kwargs.items())[1][1]

        query = db.query(self.model).filter(getattr(self.model, search_key) == search_value).filter(getattr(self.model, second_search_key) == second_search_value).all()

        if descending == True:
            data = db.query(
                self.model).filter(
                getattr(self.model, search_key) == search_value).filter(
                getattr(self.model, second_search_key) == second_search_value).order_by(
                desc(self.model.created_at)).offset(skip).limit(limit).all()
        else:
            data = db.query(self.model).filter(getattr(self.model, search_key) == search_value).filter(getattr(self.model, second_search_key) == second_search_value).offset(skip).limit(limit).all()

        if count_results == True:
            return [{"results": len(query)}, data]
        return data

    def update(self, db: Session, id: int,  data_update: UpdateSchemaType) -> ModelType:
        db.query(self.model).filter(self.model.id == id).update(
            data_update.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return self.get_one(db, id)

    def delete(self, db: Session, id: int) -> Optional[Union[ModelType, Any]]:
        result = db.query(self.model).filter(self.model.id ==
                                             id).delete(synchronize_session=False)
        db.commit()
        return result
