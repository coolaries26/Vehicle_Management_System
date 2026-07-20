from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class AuditResponse(ORMBase):

    created_by: int | None = None
    modified_by: int | None = None

    created_at: datetime | None = None
    modified_at: datetime | None = None


class MessageResponse(BaseModel):

    message: str
    success: bool = True