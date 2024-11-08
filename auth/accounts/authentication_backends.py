import datetime
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from .contants import UNSUCCESSFUL_LOGIN_CACHE_KEY
from .utils import send_warning_login_email
from accounts.monitoring.postgres import PostgresLoginMonitoring


class EmailBackend(ModelBackend):
    def log_login_attempts(self, **kwargs):
        PostgresLoginMonitoring(**kwargs).save()

    def authenticate(self, request, username=None, password=None, **kwargs):
        reject_reason = ""
        created_at = timezone.now()
        user = None
        email = username
        request = request
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            reject_reason = "User Not Exists"
            self.log_login_attempts(user=user,
                                    created_at=created_at,
                                    request=request,
                                    email=email,
                                    reject_reason=reject_reason)
            return None
        else:
            if user.login_block_until and user.login_block_until > timezone.now():
                reject_reason = "User blocked for too many attempt"
                self.log_login_attempts(user=user,
                                        created_at=created_at,
                                        request=request,
                                        email=email,
                                        reject_reason=reject_reason)
                return None
            if user.check_password(password):
                successful = True
                self.log_login_attempts(user=user,
                                        created_at=created_at,
                                        request=request,
                                        email=email,
                                        successful=successful,
                                        reject_reason=reject_reason)
                return user

            reject_reason = "Wrong password"
            self.log_login_attempts(user=user,
                                    created_at=created_at,
                                    request=request,
                                    email=email,
                                    reject_reason=reject_reason)
            cache_key = UNSUCCESSFUL_LOGIN_CACHE_KEY.format(username)
            cache.set(cache_key, cache.get(cache_key, 0) + 1, 900)
            if cache.get(cache_key) >= 5:
                send_warning_login_email(username)
                user.login_block_until = timezone.now() + datetime.timedelta(minutes=15)
                user.save()
        return None
