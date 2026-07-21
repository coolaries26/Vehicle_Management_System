from typing import Generic
from typing import TypeVar

from app.models.audit import AuditLog

class AuditRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self):

        return (
            self.db.query(AuditLog)
            .order_by(
                AuditLog.audit_id.desc()
            )
            .all()
        )