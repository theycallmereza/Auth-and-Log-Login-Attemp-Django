import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import LoginLog


@receiver(post_save, sender=LoginLog)
def detect_suspicious_logins(sender, instance, **kwargs):
    later_hour = timezone.now() - datetime.timedelta(hours=1)
    later_hour_logs = LoginLog.objects.filter(created_at__gte=later_hour, suspicious=False, successful=False)
    ip_logs = later_hour_logs.filter(ip=instance.ip)
    user_logs = later_hour_logs.filter(email=instance.email)

    if ip_logs.count() >= 10:
        ip_logs.update(suspicious=True)
    if user_logs.count() >= 10:
        user_logs.update(suspicious=True)
