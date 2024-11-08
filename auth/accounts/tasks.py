from django.core.mail import send_mail

from auth.celery import app


@app.task(name="send_celery_mail")
def send_celery_mail(subject,
                     message,
                     recipients,
                     from_email="auth@email.com", ):
    if type(recipients) == str:
        recipient_list = [recipients]
    else:
        recipient_list = recipients

    send_mail(subject, message, from_email, recipient_list)
