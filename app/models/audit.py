from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.mixins import AuditMixin, TimestampMixin
from app.db.base import Base


class AuditLog(Base,  ):

    __tablename__ = "audit_log"
    __table_args__ = {"schema": "audit"}

    audit_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    schema_name: Mapped[str | None] = mapped_column(
        String(100)
    )

    table_name: Mapped[str | None] = mapped_column(
        String(100)
    )

    record_id: Mapped[str | None] = mapped_column(
        String
    )

    operation: Mapped[str | None] = mapped_column(
        String(20)
    )

    old_data: Mapped[dict | None] = mapped_column(
        JSON
    )

    new_data: Mapped[dict | None] = mapped_column(
        JSON
    )

    changed_by: Mapped[int | None] = mapped_column(
        BigInteger
    )

    changed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime
    )