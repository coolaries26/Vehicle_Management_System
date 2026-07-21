from fastapi import APIRouter   #type: ignore
from fastapi import Depends     #type: ignore
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.audit_repository import (
    AuditRepository,
)

from app.schemas.audit import (
    AuditLogResponse,
)

from app.services.audit_service import (
    AuditService,
)

router = APIRouter(
    prefix="/api/v1/audit-logs",
    tags=["Audit Logs"],
)


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def get_audit_logs(
    db: Session = Depends(get_db),
):

    service = AuditService(
        AuditRepository(db)
    )

    return service.get_audit_logs()