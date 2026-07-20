
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy import Text, String, Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.mixins import AuditMixin,TimestampMixin

from app.db.base import Base
from app.db.mixins import AuditMixin
from app.db.mixins import TimestampMixin


from sqlalchemy import DateTime
from sqlalchemy import Text

class VehicleComplaint(
    Base,
    AuditMixin,
    TimestampMixin,
):
    __tablename__ = "vehicle_complaint"
    __table_args__ = {"schema": "maintenance"}

    complaint_id: Mapped[int] = mapped_column(primary_key=True)
    
    vehicle_id = mapped_column(
        ForeignKey(
            "master.vehicle_master.vehicle_id"
        ),
        nullable=False
    )

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("master.driver_master.driver_id"),
        nullable=False
    )

    complaint_date = mapped_column(
        DateTime,
        nullable=True
    )

    issue_description: Mapped[str | None]  = mapped_column(
        Text,
        nullable=True
    )

    driver_reason = mapped_column(
        Text,
        nullable=True
    )

    vehicle_received_at = mapped_column(
        DateTime,
        nullable=True
    )
    vehicle = relationship(
        "VehicleMaster",
        back_populates="complaints"
    )
    inspections = relationship(
        "TechnicianInspection",
        back_populates="complaint"
    )

    job_cards = relationship(
        "MaintenanceJobCard",
        back_populates="complaint"
    )
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )
    

class TechnicianInspection(
    Base,
    AuditMixin,
    TimestampMixin,
):
    __tablename__ = "technician_inspection"
    __table_args__ = {"schema": "maintenance"}

    inspection_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey(
            "maintenance.vehicle_complaint.complaint_id"
        ),nullable=False
    )

    technician_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        ),nullable=False
    )
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )

#relationships
    technician = relationship(
        "EmployeeMaster",
        back_populates="inspections"
    )

    complaint = relationship(
        "VehicleComplaint",
        back_populates="inspections"
    )

    job_cards = relationship(
        "MaintenanceJobCard",
        back_populates="inspection"
    )

    observed_issue: Mapped[str | None] = mapped_column(Text)

    operator_notes: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str | None] = mapped_column(String(30))


class MaintenanceJobCard(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = "maintenance_job_card"
    __table_args__ = {"schema": "transact"}

    job_card_id: Mapped[int] = mapped_column(primary_key=True)

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey(
            "maintenance.vehicle_complaint.complaint_id"
        ),nullable=False
    )

    inspection_id: Mapped[int] = mapped_column(
        ForeignKey(
            "maintenance.technician_inspection.inspection_id"
        ),nullable=False
    )
    
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.vehicle_master.vehicle_id"
        ),nullable=False
    )
    labour_charges: Mapped[float | None] = mapped_column(
    Numeric(12, 2)
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )

    vehicle = relationship(
        "VehicleMaster",
        back_populates="job_cards"
    )
    complaint = relationship(
        "VehicleComplaint",
        back_populates="job_cards"
    )

    inspection = relationship(
        "TechnicianInspection",
        back_populates="job_cards"
    )

    parts = relationship(
        "JobCardPart",
        back_populates="job_card"
    )

    parts = relationship(
        "JobCardPart",
        back_populates="job_card"
    )



class JobCardPart(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = "job_card_part"
    __table_args__ = {"schema": "maintenance"}

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    job_card_id: Mapped[int] = mapped_column(
        ForeignKey(
            "transact.maintenance_job_card.job_card_id"
        ),nullable=False
    )

    part_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory.part_master.part_id"
        ),nullable=False
    )

    quantity: Mapped[float | None] = mapped_column(
        Numeric(12, 2)
    )

    unit_price: Mapped[float | None] = mapped_column(
        Numeric(12, 2)
    )

    total_price: Mapped[float | None] = mapped_column(
        Numeric(12, 2)
    )
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )
    job_card = relationship(
    "MaintenanceJobCard",
    back_populates="parts"
    )
    
class PreventiveMaintenanceChecklist(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = (
        "preventive_maintenance_checklist"
    )

    __table_args__ = {
        "schema": "maintenance"
    }

    checklist_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.vehicle_master.vehicle_id"
        ),nullable=False
    )

    technician_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        ),nullable=False
    )

    observation: Mapped[str | None] = mapped_column(
        Text
    )
    vehicle = relationship(
    "VehicleMaster",
    back_populates="pm_checklists"
    )
    issue_found: Mapped[bool | None]

    issue_description: Mapped[str | None] = (
        mapped_column(Text)
    )

    maintenance_action: Mapped[
        str | None
    ] = mapped_column(Text)

    final_status: Mapped[
        str | None
    ] = mapped_column(String(30))

