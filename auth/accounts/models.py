import datetime
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .tasks import send_celery_mail


# Create your models here.

class User(AbstractUser):
    verification_code = models.IntegerField(default=0)
    code_generation_date = models.DateTimeField(null=True, blank=True)
    activation_date = models.DateTimeField(null=True, blank=True)
    login_block_until = models.DateTimeField(null=True, blank=True)

    @property
    def code_expiration(self):
        return self.code_generation_date + datetime.timedelta(seconds=300)

    @property
    def new_verification_code_allowed(self):
        if (not self.code_generation_date) or (
                (timezone.now() - self.code_generation_date).seconds > 60
        ):
            return True
        else:
            return False

    def verification_code_generator(self):
        verification_code = random.randint(100000, 999999)
        if self.new_verification_code_allowed:
            self.verification_code = verification_code
            self.code_generation_date = timezone.now()
            self.save()
            # send email
            subject = "Verification Code"
            message = str(self.verification_code)
            send_celery_mail.s(subject, message, self.email).apply_async()
            return True
        else:
            return None
