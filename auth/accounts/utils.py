from .tasks import send_celery_mail


def send_warning_login_email(email):
    subject = "Warning Email"
    message = "Too many Tries to login with your email on our service"
    send_celery_mail(subject, message, email)
