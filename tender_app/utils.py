from django.core.mail import send_mail
from django.conf import settings

def send_tender_notification(user_email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )