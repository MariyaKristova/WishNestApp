from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from WishNestApp.wishnests.models import Wishnest

UserModel = get_user_model()

class Gift(models.Model):
    wishnest = models.ForeignKey(Wishnest, on_delete=models.CASCADE, related_name='gifts')
    image = CloudinaryField('image', folder='gifts/')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='gifts')