# Generated by Django 3.2 on 2023-02-24 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0032_auto_20230224_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='price',
        ),
    ]