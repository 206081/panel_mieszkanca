# Generated by Django 3.2 on 2023-02-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0012_alter_bill_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bill",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
    ]