from fastapi import (
    APIRouter,
    Depends,
)

from fastapi.responses import (
    StreamingResponse,
)

from sqlalchemy.orm import Session

from app.db.dependencies import (
    get_db,
)

from app.repositories.part_requisition_repository import (
    PartRequisitionRepository,
)

from app.repositories.part_requisition_detail_repository import (
    PartRequisitionDetailRepository,
)

from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.repositories.employee_repository import (
    EmployeeRepository,
)

from app.repositories.part_repository import (
    PartRepository,
)

from app.services.pdf_requisition_service import (
    PDFRequisitionService,
)

router = APIRouter(
    prefix="/api/v1/requisitions_print",
    tags=["Requisition PDF"],
)


@router.get(
    "/{requisition_id}/pdf"
)
def generate_requisition_pdf(
    requisition_id: int,
    db: Session = Depends(get_db),
):

    requisition = (
        PartRequisitionRepository(db)
        .get_by_id(
            requisition_id
        )
    )

    if not requisition:

        return {
            "message":
            "Requisition not found"
        }

    vehicle = (
        VehicleRepository(db)
        .get_by_id(
            requisition.vehicle_id
        )
    )

    technician = None

    if (
        requisition.technician_id
    ):
        technician = (
            EmployeeRepository(db)
            .get_by_id(
                requisition.technician_id
            )
        )

    details = [
        item
        for item in (
            PartRequisitionDetailRepository(db)
            .get_all()
        )
        if item.requisition_id
        == requisition_id
    ]

    part_repo = (
        PartRepository(db)
    )

    part_lookup = {}

    for detail in details:

        part = (
            part_repo.get_by_id(
                detail.part_id
            )
        )

        if part:

            part_lookup[
                detail.part_id
            ] = (
                part.part_name
            )

    print(f"Requisition={requisition}")
    print(f"Vehicle={vehicle}")
    print(f"Technician={technician}")
    print(f"Details={details}")
    print(f"Part Lookup={part_lookup}")
    pdf = (
        PDFRequisitionService
        .generate_requisition_pdf(
            requisition=
                requisition,

            vehicle=
                vehicle,

            technician=
                technician,

            details=
                details,

            part_lookup=
                part_lookup,
        )
    )

    return StreamingResponse(
        pdf,
        media_type=
            "application/pdf",

        headers={
            "Content-Disposition":
            (
                "inline;"
                f' filename="requisition_{requisition_id}.pdf"'
            )
        },
    )
