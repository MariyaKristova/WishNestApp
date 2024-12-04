from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from WishNestApp.gifts.models import Gift

UserModel = get_user_model()

@receiver(post_save, sender=Gift)
def send_gift_registry_confirmation(sender, instance, created, **kwargs):
    if not created and instance.is_registered:
        send_mail(
            subject='Gift Registration Confirmation',
            from_email='WishNestMail@wishnest.com',
            message='You successfully registered for a gift',
            recipient_list=[instance.registered_by_email],
        )