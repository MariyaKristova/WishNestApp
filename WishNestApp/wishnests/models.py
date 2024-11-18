from cloudinary.models import CloudinaryField
from django.db import models
from WishNestApp.events.models import Event

class Wishnest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Gift(models.Model):
    wishnest = models.ForeignKey(Wishnest, on_delete=models.CASCADE, related_name='gifts')
    image = CloudinaryField('image', folder='gifts/')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    url = models.URLField(blank=True, null=True)