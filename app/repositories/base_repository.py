# app/repositories/base_repository.py

from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: type[ModelType],
        db: Session
    ):
        self.model = model
        self.db = db

    def create(self, obj: ModelType) -> ModelType:

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def get_all(self):

        return (
            self.db.query(self.model)
            .all()
        )

    def delete(self, obj: ModelType):

        self.db.delete(obj)
        self.db.commit()

    def save(self):

        self.db.commit()

    def refresh(self, obj: ModelType):

        self.db.refresh(obj)

        return obj
