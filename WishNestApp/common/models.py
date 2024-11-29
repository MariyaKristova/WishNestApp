import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from WishNestApp.events.models import Event


class Hug(models.Model):
    email = models.EmailField(null=True, blank=True)
    text = models.TextField(max_length=100)
    date_of_publication = models.DateTimeField(auto_now_add=True)
    to_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='hugs')


class ShareLink(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='share_links')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.event.date + timedelta(days=7)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Share link for {self.event.occasion}"