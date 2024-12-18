from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from WishNestApp.accounts.tasks import send_welcome_email
from WishNestApp.accounts.models import Profile

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        send_welcome_email.delay(instance.email)

@receiver(post_delete, sender=Profile)
def delete_user_on_profile_delete(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except UserModel.DoesNotExist:
        pass