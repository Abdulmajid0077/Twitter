from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


def send_code_to_email(email, code):
    text = f"Your verification code is: {code}"
    send_mail(
        subject='Verification Code',
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )