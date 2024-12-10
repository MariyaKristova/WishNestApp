from celery import shared_task
from django.core.mail import send_mail
from WishNestApp import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_gift_registry_email(recipient_email, gift_description, event_occasion, event_link):
    logger.info("Sending email to %s", recipient_email)
    send_mail(
        subject='Gift Registration Confirmation',
        message=(
        f'Hello, \n\n You successfully reserved a gift for event {event_occasion}: "{gift_description}"\n\n'
        f'Press link for more info about the event: {event_link}'
        ),
        from_email=settings.COMPANY_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )