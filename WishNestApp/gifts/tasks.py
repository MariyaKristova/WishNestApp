from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_gift_registry_email(recipient_email):
    send_mail(
        subject='Gift Registration Confirmation',
        from_email='WishNestMail@wishnest.com',
        message='You successfully registered for a gift!',
        recipient_list=[recipient_email],
    )