from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_future_date(value):
    if value < timezone.localdate():
        raise ValidationError('Event date cannot be in the past.')
