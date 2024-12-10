# Generated by Django 5.1.3 on 2024-12-10 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('common', '0001_initial')]

    initial = True

    dependencies = [
        ('events', '0002_rename_host_event_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('text', models.TextField(max_length=100)),
                ('date_of_publication', models.DateTimeField(auto_now_add=True)),
                ('to_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hugs', to='events.event')),
            ],
        ),
    ]
