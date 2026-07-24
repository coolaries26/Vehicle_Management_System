from sqlalchemy.orm import Session

from app.models.part_requisition import (
    PartRequisition,
)


class PartRequisitionRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        requisition: PartRequisition,
    ):

        self.db.add(requisition)
        self.db.commit()
        self.db.refresh(requisition)
        return requisition

    def get_by_id(
        self,
        requisition_id: int,
    ):

        return (
            self.db.query(
                PartRequisition
            )
            .filter(
                PartRequisition.requisition_id
                == requisition_id
            )
            .first()
        )

    def get_all(self):
        return (
            self.db.query(
                PartRequisition
            )
            .order_by(
                PartRequisition.requisition_id.desc()
            )
            .all()
        )
    def update(
        self,
        requisition,
    ):
        self.db.commit()
        self.db.refresh(
            requisition
        )
        return requisition