from datetime import datetime

from pydantic import BaseModel  #type: ignore
from pydantic import ConfigDict #type: ignore


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    audit_id: int
    schema_name: str | None = None
    table_name: str | None = None
    record_id: str | None = None
    operation: str | None = None
    old_data: dict | None = None
    new_data: dict | None = None
    changed_by: int | None = None
    changed_at: datetime | None = None