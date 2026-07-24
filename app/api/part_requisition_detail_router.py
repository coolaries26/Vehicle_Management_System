from fastapi import (APIRouter,Depends,)    #type: ignore

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.part_requisition_detail_repository import (
    PartRequisitionDetailRepository,
)

from app.schemas.part_requisition_detail_schema import (
    PartRequisitionDetailCreate,
    PartRequisitionDetailUpdate,
)

from app.services.part_requisition_detail_service import (
    PartRequisitionDetailService,
)

router = APIRouter(
    prefix=
    "/api/v1/requisition-details",
    tags=[
        "Part Requisition Details"
    ],
)


def get_service(
    db: Session =
    Depends(get_db),
):

    repository = (
        PartRequisitionDetailRepository(
            db
        )
    )

    return (
        PartRequisitionDetailService(
            repository
        )
    )


@router.post("")
def create_requisition_detail(
    payload:
    PartRequisitionDetailCreate,

    service:
    PartRequisitionDetailService =
    Depends(
        get_service
    ),
):

    return service.create(
        payload
    )


@router.get("")
def get_requisition_details(
    service:
    PartRequisitionDetailService =
    Depends(
        get_service
    ),
):

    return service.get_all()


@router.get(
    "/{requisition_detail_id}"
)
def get_requisition_detail(
    requisition_detail_id: int,

    service:
    PartRequisitionDetailService =
    Depends(
        get_service
    ),
):

    return service.get_by_id(
        requisition_detail_id
    )


@router.put(
    "/{requisition_detail_id}"
)
def update_requisition_detail(
    requisition_detail_id: int,

    payload:
    PartRequisitionDetailUpdate,

    service:
    PartRequisitionDetailService =
    Depends(
        get_service
    ),
):

    return service.update(
        requisition_detail_id,
        payload,
    )


@router.delete(
    "/{requisition_detail_id}"
)
def delete_requisition_detail(
    requisition_detail_id: int,

    service:
    PartRequisitionDetailService =
    Depends(
        get_service
    ),
):

    return service.delete(
        requisition_detail_id
    )