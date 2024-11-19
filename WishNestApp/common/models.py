from django.db import models

from WishNestApp.events.models import Event


class Hug(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField(max_length=100)
    date_of_publication = models.DateTimeField(auto_now_add=True)
    to_event = models.ForeignKey(Event, on_delete=models.CASCADE)