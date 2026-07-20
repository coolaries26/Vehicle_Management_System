from datetime import date
from app.db.mixins import AuditMixin,TimestampMixin

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class EmployeeMaster(Base,AuditMixin,TimestampMixin,):

    __tablename__ = "employee_master"
    __table_args__ = {"schema": "master"}

    employee_id: Mapped[int] = mapped_column(primary_key=True)

    employee_type: Mapped[str | None] = mapped_column(String(30))

    full_name: Mapped[str | None] = mapped_column(String(100))

    phone_number: Mapped[str] = mapped_column(String(15))
    
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )
    inspections = relationship(
        "TechnicianInspection",
        back_populates="technician"
    )


class DriverMaster(Base,AuditMixin,TimestampMixin):

    __tablename__ = "driver_master"
    __table_args__ = {"schema": "master"}

    driver_id: Mapped[int] = mapped_column(primary_key=True)

    driver_name: Mapped[str] = mapped_column(String(200))

    mobile_number: Mapped[str] = mapped_column(String(20))

    dl_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True
    )

    dl_expiry_date: Mapped[date | None] = mapped_column(Date)
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )



class VehicleMaster(Base,AuditMixin,TimestampMixin):

    __tablename__ = "vehicle_master"
    __table_args__ = {"schema": "master"}

    vehicle_id: Mapped[int] = mapped_column(
        primary_key=True
    )
    
    vehicle_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "reference.vehicle_type_ref.vehicle_type_id"
        ),
        nullable=True,
    )
    
    fuel_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "reference.fuel_type_ref.fuel_type_id"
        ),
        nullable=True,
    )
    
    vehicle_status_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "reference.vehicle_status_ref.vehicle_status_id"
        ),
        nullable=True,
    )
    
    rc_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    
    purchase_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    
    rc_expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    
    engine_no: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )
    
    chassis_no: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )
    
    gps_id: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
    )
    
    fuel_capacity: Mapped[float | None] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )
    
    active_flag: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True,
        nullable=True,
    )

    complaints = relationship(
        "VehicleComplaint",
        back_populates="vehicle"
    )
    
    job_cards = relationship(
        "MaintenanceJobCard",
        back_populates="vehicle"
    )
    pm_checklists = relationship(
        "PreventiveMaintenanceChecklist",
        back_populates="vehicle"
    )

