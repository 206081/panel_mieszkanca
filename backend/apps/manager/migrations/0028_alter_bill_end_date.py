# Generated by Django 3.2 on 2023-02-24 14:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0027_alter_bill_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]