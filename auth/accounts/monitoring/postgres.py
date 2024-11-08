from .base import LoginMonitoring
from accounts.models import LoginLog


class PostgresLoginMonitoring(LoginMonitoring):
    def __init__(self, user, created_at, request, successful=False, suspicious=False, reject_reason="", email=None):
        self.user_id = user.pk if user else None
        self.email = user.email if user else email
        self.ip = self.get_client_ip(request)
        self.user_agent = request.META["HTTP_USER_AGENT"]
        self.created_at = created_at
        self.successful = successful
        self.suspicious = suspicious
        self.reject_reason = reject_reason

    def save(self):
        obj = LoginLog(
            user_id=self.user_id,
            email=self.email,
            ip=self.ip,
            user_agent=self.user_agent,
            created_at=self.created_at,
            successful=self.successful,
            suspicious=self.suspicious,
            reject_reason=self.reject_reason
        )
        obj.save()
        return obj
