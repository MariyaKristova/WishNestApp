# from celery import shared_task
# from django.core.mail import send_mail
# from WishNestApp import settings
#
#
# @shared_task
# def send_gift_registry_email(recipient_email):
#     send_mail(
#         subject='Gift Registration Confirmation',
#         message='You successfully registered for a gift!',
#         from_email=settings.COMPANY_EMAIL,
#         recipient_list=[recipient_email],
#         fail_silently=False,
#     )


from celery import shared_task
from django.core.mail import send_mail
import logging
from WishNestApp import settings

logger = logging.getLogger(__name__)

@shared_task
def send_gift_registry_email(recipient_email):
    try:
        logger.info(f"Attempting to send email to {recipient_email}")
        send_mail(
            subject='Gift Registration Confirmation',
            message='You successfully registered for a gift!',
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
