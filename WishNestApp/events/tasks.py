from celery import shared_task
from .models import Event

@shared_task
def delete_expired_events():
    expired_events = Event.objects.all()
    count = 0

    for event in expired_events:
        if event.is_expired_for_deletion:
            event.delete()
            count += 1

    if count > 0:
        print(f"{count} expired events deleted.")
    else:
        print("No expired events found.")
    return count

