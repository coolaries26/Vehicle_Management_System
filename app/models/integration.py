
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.db.mixins import AuditMixin,TimestampMixin

class WhatsAppMessageLog(Base,
    AuditMixin,
    TimestampMixin,
                         ):

    __tablename__ = "whatsapp_message_log"
    __table_args__ = {"schema": "integration"}

    message_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    approval_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "inventory.approval_request.approval_id"
        )
    )

    recipient_mobile: Mapped[str] = mapped_column(
        String(20)
    )

    send_status: Mapped[str | None] = mapped_column(
        String(30)
    )

class ApprovalRequest(Base,
    AuditMixin,
    TimestampMixin,
                      ):

    __tablename__ = "approval_request"
    __table_args__ = {"schema": "inventory"}

    approval_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    request_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory.part_request.request_id"
        )
    )

    approver_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        )
    )