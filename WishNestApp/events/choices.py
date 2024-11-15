from django.db import models

class EventChoices(models.TextChoices):
    BIRTHDAY = 'Birthday', 'Birthday'
    WEDDING = 'Wedding', 'Wedding'
    BABY_SHOWER = 'Baby Shower', 'Baby Shower'
    GRADUATION = 'Graduation', 'Graduation'
    ANNIVERSARY = 'Anniversary', 'Anniversary'
    HOUSE_WARMING = 'House Warming', 'House Warming'
    OTHER = 'Other', 'Other'