
class AuditService:

    def __init__(self, repo):
        self.repo = repo

    def get_audit_logs(self):
        return self.repo.get_all()