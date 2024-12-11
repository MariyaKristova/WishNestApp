from celery import shared_task
from django.core.mail import send_mail
from WishNestApp import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(recipient_email):
    logger.info("Sending welcome email to %s", recipient_email)
    if not settings.TESTING:
        send_mail(
            subject="Welcome to WishNest",
            message="Hello, \n\n You successfully created your profile. \n\n Create events, share your wishes, and make them come true!",
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
