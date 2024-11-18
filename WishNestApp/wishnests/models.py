from django.contrib.auth import get_user_model
from django.db import models

from WishNestApp.accounts.models import CustomUser
from WishNestApp.events.models import Event

UserModel = get_user_model()

class Wishnest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='wishnests')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='wishnests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
