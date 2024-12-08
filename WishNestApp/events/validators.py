from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import datetime
from django.utils import timezone


def validate_future_date(value):
    event_datetime = datetime.combine(value, datetime.min.time())
    event_datetime = timezone.make_aware(event_datetime)

    if event_datetime < now():
        raise ValidationError('Event date cannot be in the past.')
