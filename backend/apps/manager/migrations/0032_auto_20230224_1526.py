# Generated by Django 3.2 on 2023-02-24 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0031_auto_20230224_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billtype',
            name='subtype',
        ),
        migrations.DeleteModel(
            name='BillSubType',
        ),
    ]