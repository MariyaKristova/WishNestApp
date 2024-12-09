from celery import shared_task
from django.utils import timezone
from WishNestApp.common.models import ShareLink

@shared_task
def delete_expired_sharelinks():
    expired_links = ShareLink.objects.filter(expires_at__lt=timezone.now())
    count, _ = expired_links.delete()
    if count > 0:
        print(f"{count} expired share links deleted.")
    else:
        print("No expired share links found.")
    return count

@shared_task
def test_task():
    print("Test task executed successfully!")