# Generated by Django 3.2 on 2023-02-18 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0010_auto_20230218_0748"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apartment",
            old_name="amount",
            new_name="balance",
        ),
    ]
