
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.mixins import AuditMixin,TimestampMixin

from app.db.base import Base
from app.db.mixins import AuditMixin
from app.db.mixins import TimestampMixin


class DriverVehicleAssignment(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = "driver_vehicle_assignment"
    __table_args__ = {"schema": "operations"}

    assignment_id: Mapped[int] = mapped_column(primary_key=True)

    driver_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.driver_master.driver_id"
        )
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.vehicle_master.vehicle_id"
        )
    )

    driver = relationship("DriverMaster")

    vehicle = relationship("VehicleMaster")
