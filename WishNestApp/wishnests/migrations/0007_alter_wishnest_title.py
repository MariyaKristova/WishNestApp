# Generated by Django 5.1.3 on 2024-11-21 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishnests', '0006_alter_wishnest_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishnest',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
