# Generated by Django 3.2 on 2023-02-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0038_housingbill_housing'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='account',
            field=models.DecimalField(decimal_places=0, default=52849419115624054411755520, max_digits=26),
        ),
    ]