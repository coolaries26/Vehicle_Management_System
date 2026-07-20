from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func


class TimestampMixin:

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )

    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class AuditMixin:

    created_by: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    modified_by: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )