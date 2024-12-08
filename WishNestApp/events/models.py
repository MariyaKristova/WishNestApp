from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.utils.timezone import now
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
        event_datetime = datetime.combine(self.date, self.time)
        event_datetime = make_aware(event_datetime)
        return event_datetime < now()

    @property
    def is_expired_for_deletion(self):
        event_datetime = datetime.combine(self.date, self.time)
        event_datetime = make_aware(event_datetime)
        return event_datetime + timedelta(days=7) < now()