# Generated by Django 3.2 on 2023-02-24 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0033_remove_bill_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]