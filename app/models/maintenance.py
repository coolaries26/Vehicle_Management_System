
from datetime import datetime
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
        ForeignKey("maintenance.vehicle_complaint.complaint_id"),nullable=False
    )
    inspection_id: Mapped[int] = mapped_column(
        ForeignKey("maintenance.technician_inspection.inspection_id"),nullable=False
    )
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("master.vehicle_master.vehicle_id"),nullable=False
    )
    labour_charges: Mapped[float | None] = mapped_column(Numeric(12, 2)
    )
    description: Mapped[str | None] = mapped_column(Text,nullable=True
    )
    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey("master.driver_master.driver_id")
    )

    technician1_id: Mapped[int | None] = mapped_column(
        ForeignKey("master.employee_master.employee_id")
    )

    technician2_id: Mapped[int | None] = mapped_column(
        ForeignKey("master.employee_master.employee_id")
    )

    date_time_in: Mapped[datetime | None]

    date_time_out: Mapped[datetime | None]

    zone_area: Mapped[str | None] = mapped_column(
        String(200)
    )

    mileage_hours: Mapped[str | None] = mapped_column(
        String(100)
    )

    maintenance_type: Mapped[str | None] = mapped_column(
        String(50)
    )

    issue_reported: Mapped[str | None] = mapped_column(
        Text
    )
    requested_by_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("master.employee_master.employee_id")
    )
    
    verified_by_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("master.employee_master.employee_id")
    )
    
    approved_by_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("master.employee_master.employee_id")
    )
    
    job_status: Mapped[str | None] = mapped_column(
        String(50),
        default="OPEN"
    )
    problem_found_action_taken: Mapped[
        str | None
    ] = mapped_column(Text)

    requisition_slip_number: Mapped[
        str | None
    ] = mapped_column(String(100))

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
    __tablename__ = ("preventive_maintenance_checklist")
    __table_args__ = {"schema": "maintenance"}
    checklist_id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("master.vehicle_master.vehicle_id"),nullable=False)
    technician_id: Mapped[int] = mapped_column(
        ForeignKey("master.employee_master.employee_id"),nullable=False)
    observation: Mapped[str | None] = mapped_column(Text)
    vehicle = relationship("VehicleMaster",back_populates="pm_checklists")
    issue_found: Mapped[bool | None]
    issue_description: Mapped[str | None] = (mapped_column(Text))
    maintenance_action: Mapped[str | None] = mapped_column(Text)
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )

    final_status: Mapped[    str | None] = mapped_column(String(30))

