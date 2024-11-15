from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
UserModel = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    profile_image = CloudinaryField('image', folder='profile_images/')