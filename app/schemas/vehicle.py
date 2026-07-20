from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class VehicleCreate(BaseModel):

    vehicle_type_id: int | None = None
    fuel_type_id: int | None = None
    vehicle_status_id: int | None = None

    rc_number: str = Field(
        min_length=5,
        max_length=50
    )

    purchase_date: date | None = None
    rc_expiry_date: date | None = None

    engine_no: str | None = None
    chassis_no: str | None = None
    gps_id: str | None = None

    fuel_capacity: float | None = None
    active_flag: bool | None = True


class VehicleUpdate(BaseModel):

    vehicle_type_id: int | None = None
    fuel_type_id: int | None = None
    vehicle_status_id: int | None = None

    rc_number: str | None = Field(
        default=None,
        min_length=5,
        max_length=50
    )

    purchase_date: date | None = None
    rc_expiry_date: date | None = None

    engine_no: str | None = None
    chassis_no: str | None = None
    gps_id: str | None = None

    fuel_capacity: float | None = None
    active_flag: bool | None = None


class VehicleResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    vehicle_id: int

    vehicle_type_id: int | None = None
    fuel_type_id: int | None = None
    vehicle_status_id: int | None = None

    rc_number: str

    purchase_date: date | None = None
    rc_expiry_date: date | None = None

    engine_no: str | None = None
    chassis_no: str | None = None
    gps_id: str | None = None

    fuel_capacity: float | None = None
    active_flag: bool | None = True

    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None