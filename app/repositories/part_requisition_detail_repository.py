from sqlalchemy.orm import Session

from app.models.part_requisition import (
    PartRequisitionDetail,
)


class PartRequisitionDetailRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        detail: PartRequisitionDetail,
    ):

        self.db.add(detail)

        self.db.commit()

        self.db.refresh(detail)

        return detail

    def get_by_id(
        self,
        requisition_detail_id: int,
    ):

        return (
            self.db.query(
                PartRequisitionDetail
            )
            .filter(
                PartRequisitionDetail.requisition_detail_id
                == requisition_detail_id
            )
            .first()
        )

    def get_all(
        self,
    ):

        return (
            self.db.query(
                PartRequisitionDetail
            )
            .order_by(
                PartRequisitionDetail.requisition_detail_id.desc()
            )
            .all()
        )

    def update(
        self,
        detail,
    ):

        self.db.commit()

        self.db.refresh(detail)

        return detail