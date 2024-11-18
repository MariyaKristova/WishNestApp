# Generated by Django 5.1.3 on 2024-11-18 15:57

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wishnests', '0002_delete_gift'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('wishnest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gifts', to='wishnests.wishnest')),
            ],
        ),
    ]
