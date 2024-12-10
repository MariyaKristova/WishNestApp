from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from WishNestApp import settings
from WishNestApp.gifts.models import Gift
from WishNestApp.gifts.tasks import send_gift_registry_email

UserModel = get_user_model()

@receiver(post_save, sender=Gift)
def send_gift_registry_confirmation(sender, instance, created, **kwargs):
    if not created and instance.is_registered:
        event_occasion = instance.wishnest.event.occasion
        share_link = instance.wishnest.event.share_links.first()
        if share_link:
            event_link = f"{settings.SITE_URL}{reverse('shared-event', args=[share_link.token])}"
        else:
            event_link = "Event link unavailable."

        send_gift_registry_email.delay(
            instance.registered_by_email,
            instance.description,
            event_occasion,
            event_link,
        )