# Generated by Django 5.1.3 on 2024-12-09 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0011_alter_gift_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='description',
            field=models.TextField(),
        ),
    ]