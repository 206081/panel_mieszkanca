# Generated by Django 3.2 on 2023-02-18 06:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0006_auto_20230217_2254"),
    ]

    operations = [
        migrations.CreateModel(
            name="BillType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="bill",
            name="apartment",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, related_name="apartment", to="manager.apartment"
            ),
        ),
        migrations.AddField(
            model_name="bill",
            name="bill_type",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="bill_type", to="manager.billtype"
            ),
        ),
    ]
