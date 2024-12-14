from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from WishNestApp.accounts.models import Profile
from WishNestApp.events.choices import EventChoices
from WishNestApp.events.validators import validate_future_date

UserModel = get_user_model()

class Event(models.Model):
    occasion = models.CharField(choices=EventChoices.choices, default=EventChoices.PARTY)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='events')
    date = models.DateField(validators=[validate_future_date])
    time = models.TimeField()
    location = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_past(self):
        return self.date < timezone.localdate()

    @property
    def is_expired_for_deletion(self):
        return (self.date + timedelta(days=7)) < timezone.localdate()