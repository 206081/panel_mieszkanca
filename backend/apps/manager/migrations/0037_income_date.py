# Generated by Django 3.2 on 2023-02-25 07:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0036_auto_20230224_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
