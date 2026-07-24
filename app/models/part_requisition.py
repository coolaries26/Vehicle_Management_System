from sqlalchemy import ForeignKey,String,Text,Boolean,DateTime,Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.mixins import AuditMixin,TimestampMixin

from app.db.base import Base



from datetime import datetime




class PartRequisition(Base):

    __tablename__ = "part_requisition"
    __table_args__ = {
        "schema": "transact"
    }

    requisition_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    requisition_number: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
    )

    requisition_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.vehicle_master.vehicle_id"
        )
    )

    job_card_id: Mapped[int] = mapped_column(
        ForeignKey(
            "transact.maintenance_job_card.job_card_id"
        )
    )

    technician_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        )
    )

    remarks: Mapped[str | None] = mapped_column(
        Text
    )

    status: Mapped[str | None] = mapped_column(
        String(30),
        default="OPEN",
    )

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_by: Mapped[int | None] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    modified_by: Mapped[int | None] = mapped_column(
        nullable=True
    )

    modified_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

class PartRequisitionDetail(Base):

    __tablename__ = (        "part_requisition_detail")

    __table_args__ = {        "schema": "transact"    }

    requisition_detail_id: Mapped[int] = mapped_column(primary_key=True)

    requisition_id: Mapped[int] = mapped_column(
        ForeignKey(            "transact.part_requisition.requisition_id")
    )

    part_id: Mapped[int] = mapped_column(
        ForeignKey(            "inventory.part_master.part_id")
    )

    quantity_required: Mapped[float | None] = mapped_column(
        Numeric(10, 2)
    )

    quantity_returned: Mapped[float | None] = mapped_column(
        Numeric(10, 2)
    )

    required_serial_number: Mapped[str | None] = mapped_column(
        String(200)
    )

    returned_serial_number: Mapped[str | None] = mapped_column(
        String(200)
    )

    remarks: Mapped[str | None] = mapped_column(
        Text
    )

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )