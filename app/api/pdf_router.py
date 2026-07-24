from fastapi import APIRouter   #type: ignore
from fastapi import Depends     #type: ignore
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from fastapi.responses import (    StreamingResponse,)  #type: ignore

from app.services.pdf_service import (    PDFService,)
from app.repositories.vehicle_repository import (    VehicleRepository,)
from app.repositories.driver_repository import (    DriverRepository,)
from app.repositories.employee_repository import (    EmployeeRepository,)
from app.repositories.jobcard_repository import (    JobCardRepository,)
from app.repositories.jobcard_part_repository import (    JobCardPartRepository,)
from app.repositories.part_repository import (    PartRepository,)


router = APIRouter(
    prefix="/api/v1/jobcards_print",
    tags=["Prepare pdf to download"],
)


@router.get(    "/{job_card_id}/pdf")

def generate_jobcard_pdf(
    job_card_id: int,
    db: Session =
        Depends(get_db),
):
    part_repo = PartRepository(db)
    part_lookup = {}
    job_card = (
        JobCardRepository(db).get_by_id(job_card_id)
    )
    vehicle = None
    driver = None
    technician1 = None
    technician2 = None
    requested_by = None
    verified_by = None
    approved_by = None
    parts = []
    if job_card.vehicle_id:
        vehicle = (
            VehicleRepository(db)
            .get_by_id(
                job_card.vehicle_id
            )
        )
    if job_card.driver_id:
        driver = (
            DriverRepository(db)
            .get_by_id(
                job_card.driver_id
            )
        )
    if job_card.technician1_id:
        technician1 = (
            EmployeeRepository(db)
            .get_by_id(
                job_card.technician1_id
            )
        )
    if job_card.technician2_id:
        technician2 = (
            EmployeeRepository(db)
            .get_by_id(
                job_card.technician2_id
            )
        )
    if job_card.requested_by_employee_id:
        requested_by = (
            EmployeeRepository(db)
            .get_by_id(
                job_card.requested_by_employee_id
            )
        )
    if job_card.verified_by_employee_id:
        verified_by = (
            EmployeeRepository(db)
            .get_by_id(
                job_card.verified_by_employee_id
            )
        )
    if job_card.approved_by_employee_id:
        approved_by = (
            EmployeeRepository(db)
            .get_by_id(
                job_card.approved_by_employee_id
            )
        )
    parts = (
    JobCardPartRepository(db).get_by_jobcard(
        job_card_id
    ))
    for item in parts:
        master_part = (
            part_repo.get_by_id(
                item.part_id
            )
        )    
        if master_part:
            part_lookup[
                item.part_id
            ] = master_part.part_name

    print(job_card)
    pdf = PDFService.generate_job_card_pdf(
            job_card=job_card,
            vehicle=vehicle,
            driver=driver,
            technician1=technician1,
            technician2=technician2,
            requested_by=requested_by,
            verified_by=verified_by,
            approved_by=approved_by,
            parts=parts,
            part_lookup=part_lookup,
            )
        
    return StreamingResponse(
        pdf,
        media_type=
            "application/pdf",
        headers={
            "Content-Disposition":
            (
              f'inline; '
              f'filename='
              f'"jobcard_'
              f'{job_card_id}.pdf"'
            )
        },
    )
