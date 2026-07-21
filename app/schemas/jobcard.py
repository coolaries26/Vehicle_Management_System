from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel  #type: ignore
from pydantic import ConfigDict #type: ignore

#Create JobCard
class JobCardCreate(BaseModel):
    complaint_id: int
    inspection_id: int
    vehicle_id: int
    maintenance_type_id: int | None = None
    severity_id: int | None = None
    labour_charges: float | None = None
    description: str | None = None
    active_flag: bool | None = True
#job card enhanement
    driver_id: int | None = None
    technician1_id: int | None = None
    technician2_id: int | None = None
    date_time_in: datetime | None = None
    date_time_out: datetime | None = None
    zone_area: str | None = None
    mileage_hours: str | None = None
    maintenance_type: str | None = None
    issue_reported: str | None = None
    problem_found_action_taken: str | None = None
    requisition_slip_number: str | None = None

#Update
class JobCardUpdate(BaseModel):
    severity_id: int | None = None
    labour_charges: float | None = None
    job_status: str | None = None
    job_card_status: str | None = None
    description: str | None = None
    downtime_hours: float | None = None
    completion_date: date | None = None
    active_flag: bool | None = True
# Job card enhancement
    driver_id: int | None = None
    technician1_id: int | None = None
    technician2_id: int | None = None
    date_time_in: datetime | None = None
    date_time_out: datetime | None = None
    zone_area: str | None = None
    mileage_hours: str | None = None
    maintenance_type: str | None = None
    issue_reported: str | None = None
    problem_found_action_taken: str | None = None
    requisition_slip_number: str | None = None



#Response
class JobCardResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    job_card_id: int
    vehicle_id: int
    complaint_id: int
    inspection_id: int

    description: str | None = None
    labour_charges: float | None = None

    maintenance_type_id: int | None = None
    severity_id: int | None = None
    completion_date: date | None = None
    active_flag: bool | None = True

    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None
# Job card enhancement
    driver_id: int | None = None
    technician1_id: int | None = None
    technician2_id: int | None = None
    date_time_in: datetime | None = None
    date_time_out: datetime | None = None
    zone_area: str | None = None
    mileage_hours: str | None = None
    maintenance_type: str | None = None
    issue_reported: str | None = None
    problem_found_action_taken: str | None = None
    requisition_slip_number: str | None = None
