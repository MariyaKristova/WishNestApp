# Generated by Django 5.1.3 on 2024-12-09 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0009_remove_gift_registered_by_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
