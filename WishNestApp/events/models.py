from django.db import models
from django.contrib.auth import get_user_model
from WishNestApp.accounts.models import Profile
from WishNestApp.events.choices import EventChoices

UserModel = get_user_model()

class Event(models.Model):
    occasion = models.CharField(choices=EventChoices.choices, default=EventChoices.OTHER)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)