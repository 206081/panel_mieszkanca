# Generated by Django 3.2 on 2023-02-17 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0004_auto_20230217_1843"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Bills",
            new_name="Bill",
        ),
    ]
