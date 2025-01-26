from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlmodel import SQLModel

from app.api.error import Exception404
from app.db.base import Base
from app.utils.logger import make_logger

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


logger = make_logger(__name__)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], db: Session):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    def get_count(self) -> int:
        return self.db.query(self.model).count()

    def get_all(self) -> list[ModelType]:
        return self.db.query(self.model).all()

    def get_by_id(self, *, id: Any) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_by_conditions(self, *, conditions: bool = False) -> ModelType | None:
        return self.db.query(self.model).filter(conditions).first()

    def get_all_by_conditions(self, *, conditions: bool = False) -> list[ModelType]:
        return self.db.query(self.model).filter(conditions).all()

    def get_by_pagination(
        self, *, offset: int = 0, limit: int = 10, conditions: bool = False
    ) -> list[ModelType]:
        return (
            self.db.query(self.model)
            .filter(conditions if conditions else True)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)

        return db_obj

    def update(
        self, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, *, id: int) -> ModelType | None:
        obj = self.db.query(self.model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj

    def delete_by_conditions(self, *, conditions: bool) -> int:
        try:
            removed_cnt = self.db.query(self.model).filter(conditions).delete()
        except UnmappedInstanceError as e:
            raise Exception404(detail=str(e))

        return removed_cnt
