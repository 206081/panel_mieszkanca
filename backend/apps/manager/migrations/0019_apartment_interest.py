# Generated by Django 3.2 on 2023-02-23 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_apartment_occupant'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='interest',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]