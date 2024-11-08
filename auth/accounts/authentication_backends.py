import datetime
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from .contants import UNSUCCESSFUL_LOGIN_CACHE_KEY
from .utils import send_warning_login_email


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.login_block_until and user.login_block_until > timezone.now():
                return None
            if user.check_password(password):
                return user

            cache_key = UNSUCCESSFUL_LOGIN_CACHE_KEY.format(username)
            cache.set(cache_key, cache.get(cache_key, 0) + 1, 900)
            if cache.get(cache_key) >= 5:
                send_warning_login_email(username)
                user.login_block_until = timezone.now() + datetime.timedelta(minutes=15)
                user.save()
        return None
