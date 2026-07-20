
# app/repositories/part_repository.py


from sqlalchemy.orm import Session

from app.models.inventory import (
    PartMaster,
)

from app.repositories.base_repository import (
    BaseRepository,
)

class PartRepository:

    def __init__(self, db):
        self.db = db

    def create(self, part):
        self.db.add(part)
        self.db.commit()
        self.db.refresh(part)
        return part

    def get_all(self):
        return (
            self.db.query(
                PartMaster
            ).all()
        )

    def get_by_id(
        self,
        part_id: int
    ):
        return (
            self.db.query(
                PartMaster
            )
            .filter(
                PartMaster.part_id
                == part_id
            )
            .first()
        )
    def update_part(
        self,
        part: PartMaster,
        data: dict,
    ) -> PartMaster:

        for key, value in data.items():

            setattr(
                part,
                key,
                value,
            )

        self.db.commit()

        self.db.refresh(
            part
        )

        return part

    def delete_part(
        self,
        part: PartMaster,
    ) -> None:

        self.db.delete(
            part
        )

        self.db.commit()
    
    def exists(
    self,
    part_id: int
    ) -> bool:
    
        return (
            self.get_by_id(part_id)
            is not None
        )