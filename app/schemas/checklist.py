from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel  #type: ignore
from pydantic import ConfigDict #type: ignore


class PMChecklistCreate(BaseModel):
    vehicle_id: int
    technician_id: int
    observation: str | None = None
    issue_found: bool = False
    issue_description: str | None = None
    maintenance_action: str | None = None
    final_status: str | None = None
    active_flag: bool | None = True

class PMChecklistUpdate(BaseModel):
    vehicle_id: int | None = None
    technician_id: int | None = None
    observation: str | None = None
    issue_found: bool | None = None
    issue_description: str | None = None
    maintenance_action: str | None = None
    final_status: str | None = None
    active_flag: bool | None = None

class PMChecklistResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )
    checklist_id: int
    vehicle_id: int
    technician_id: int
    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None
    observation: str | None = None
    issue_found: bool | None = None
    issue_description: str | None = None
    maintenance_action: str | None = None
    final_status: str | None = None
    active_flag: bool | None = True
