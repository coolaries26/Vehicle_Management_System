from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel  #type: ignore
from pydantic import ConfigDict #type: ignore

#InspectionCreate
class InspectionCreate(BaseModel):
    complaint_id: int
    technician_id: int
    observed_issue: str | None = None
    operator_notes: str | None = None
    status: str | None = None
    active_flag: bool | None = True


#InspectionUpdate
class InspectionUpdate(BaseModel):
    complaint_id: int | None = None
    technician_id: int | None = None
    
    observed_issue: str | None = None
    operator_notes: str | None = None
    status: str | None = None
    active_flag: bool | None = True

#InspectionResponse
class InspectionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    inspection_id: int
    complaint_id: int
    technician_id: int
    observed_issue: str | None = None
    operator_notes: str | None = None
    status: str | None = None
    inspection_time: datetime | None = None
    active_flag: bool | None = True
    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None