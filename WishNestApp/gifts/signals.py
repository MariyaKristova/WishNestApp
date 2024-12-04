from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from WishNestApp.gifts.models import Gift
from WishNestApp.gifts.tasks import send_gift_registry_email

UserModel = get_user_model()

@receiver(post_save, sender=Gift)
def send_gift_registry_confirmation(sender, instance, created, **kwargs):
    if not created and instance.is_registered:
        send_gift_registry_email.delay(instance.registered_by_email)