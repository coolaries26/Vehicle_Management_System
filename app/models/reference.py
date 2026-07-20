from sqlalchemy import String
from sqlalchemy import SmallInteger, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base

#VehicleTypeRef
class VehicleTypeRef(Base,
                     ):
    __tablename__ = "vehicle_type_ref"
    __table_args__ = {"schema": "reference"}

    vehicle_type_id = mapped_column(
        SmallInteger,
        primary_key=True
    )

    vehicle_type_name = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

#MaintenanceTypeRef
class MaintenanceTypeRef(Base,
                         ):
    __tablename__ = "maintenance_type_ref"
    __table_args__ = {"schema": "reference"}

    maintenance_type_id = mapped_column(
        Integer,
        primary_key=True
    )

    maintenance_type_name = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

#Severity
class Severity(Base,
               ):
    __tablename__ = "severity"
    __table_args__ = {"schema": "reference"}

    severity_id = mapped_column(
        SmallInteger,
        primary_key=True
    )

    severity_name = mapped_column(
        String,
        unique=True
    )

#FuelTypeRef
class FuelTypeRef(Base,
                  ):
    __tablename__ = "fuel_type_ref"
    __table_args__ = {"schema": "reference"}

    fuel_type_id = mapped_column(
        SmallInteger,
        primary_key=True
    )

    fuel_type_name = mapped_column(
        String,
        unique=True
    )
class VehicleStatusRef(Base):

    __tablename__ = "vehicle_status_ref"
    __table_args__ = {"schema": "reference"}

    vehicle_status_id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
    )

    vehicle_status_name: Mapped[str | None] = mapped_column(
        String,
        unique=True,
    )