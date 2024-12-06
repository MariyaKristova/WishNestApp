from celery import shared_task
from django.core.mail import send_mail
from WishNestApp import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_gift_registry_email(recipient_email):
    logger.info("Sending email to %s", recipient_email)
    send_mail(
        subject='Gift Registration Confirmation',
        message='You successfully registered for a gift!',
        from_email=settings.COMPANY_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )