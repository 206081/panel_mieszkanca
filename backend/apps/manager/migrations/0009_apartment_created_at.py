# Generated by Django 3.2 on 2023-02-18 07:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0008_auto_20230218_0711"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now, verbose_name="Registered at"
            ),
            preserve_default=False,
        ),
    ]