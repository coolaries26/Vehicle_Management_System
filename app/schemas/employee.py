from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class EmployeeCreate(BaseModel):
    employee_type: str
    full_name: str
    phone_number: str
    active_flag: bool | None = True



class EmployeeUpdate(BaseModel):
    employee_type: str | None = None
    full_name: str | None = None
    phone_number: str | None = None
    active_flag: bool | None = True


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    employee_id: int
    employee_type: str
    full_name: str
    phone_number: str
    active_flag: bool | None = True
    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None