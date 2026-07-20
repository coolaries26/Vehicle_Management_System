from __future__ import annotations
from datetime import date
from datetime import datetime


from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class DriverCreate(BaseModel):
    driver_name: str = Field(
        min_length=2,
        max_length=200
    )
    mobile_number: str
    dl_number: str | None = None
    dl_expiry_date: date | None = None
    permanent_address: str | None = None
    current_address: str | None = None
    active_flag: bool | None = True



class DriverUpdate(BaseModel):
    driver_name: str | None = None
    mobile_number: str | None = None
    dl_number: str | None = None
    dl_expiry_date: date | None = None
    permanent_address: str | None = None
    current_address: str | None = None
    active_flag: bool | None = True


class DriverResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    driver_id: int
    driver_name: str
    mobile_number: str
    dl_number: str | None = None
    active_flag: bool | None = True
    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None