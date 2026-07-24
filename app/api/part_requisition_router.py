from fastapi import (    APIRouter,Depends,)    #type: ignore

from sqlalchemy.orm import Session

#from app.db.session import (    get_db, )   #type: ignore
from app.db.dependencies import get_db

from app.repositories.part_requisition_repository import (
    PartRequisitionRepository,
)

from app.schemas.part_requisition_schema import (
    PartRequisitionCreate,
    PartRequisitionUpdate,
    PartRequisitionResponse
)

from app.services.part_requisition_service import (
    PartRequisitionService,
)

router = APIRouter(
    prefix=
    "/api/v1/requisitions",
    tags=[
        "Part Requisitions"
    ],
)


def get_service(
    db: Session =
    Depends(get_db),
):

    repository = (
        PartRequisitionRepository(
            db
        )
    )

    return (
        PartRequisitionService(
            repository
        )
    )


@router.post("")
def create_requisition(
    payload:
    PartRequisitionCreate,
    service:
    PartRequisitionService =
    Depends(
        get_service
    ),
):

    return (
        service.create(
            payload
        )
    )


@router.get("")
def get_requisitions(
    service:
    PartRequisitionService =
    Depends(
        get_service
    ),
):

    return (
        service.get_all()
    )


@router.get(
    "/{requisition_id}",
    response_model=PartRequisitionResponse,
)
def get_requisition(
    requisition_id: int,
    service:
    PartRequisitionService =
    Depends(
        get_service
    ),
):

    return (
        service.get_by_id(
            requisition_id
        )
    )


@router.put(
    "/{requisition_id}"
)
def update_requisition(
    requisition_id: int,

    payload:
    PartRequisitionUpdate,

    service:
    PartRequisitionService =
    Depends(
        get_service
    ),
):

    return (
        service.update(
            requisition_id,
            payload,
        )
    )


@router.delete(
    "/{requisition_id}"
)
def delete_requisition(
    requisition_id: int,

    service:
    PartRequisitionService =
    Depends(
        get_service
    ),
):

    return (
        service.delete(
            requisition_id
        )
    )