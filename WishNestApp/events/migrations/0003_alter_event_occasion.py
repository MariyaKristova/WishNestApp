# Generated by Django 5.1.3 on 2024-11-19 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_rename_host_event_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='occasion',
            field=models.CharField(choices=[('Birthday', 'Birthday'), ('Wedding', 'Wedding'), ('Baby Shower', 'Baby Shower'), ('Graduation', 'Graduation'), ('Anniversary', 'Anniversary'), ('House Warming', 'House Warming'), ('New Year', 'New Year'), ('Christmas', 'Christmas'), ('Party', 'Party')], default='Party'),
        ),
    ]