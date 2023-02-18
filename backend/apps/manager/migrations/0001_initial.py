# Generated by Django 3.2 on 2022-10-01 20:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Apartment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("address", models.CharField(max_length=100, unique=True, verbose_name="Address")),
                ("postal_code", models.CharField(max_length=6, verbose_name="PostalCode")),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True)),
                ("account_number", models.IntegerField()),
                ("area", models.IntegerField()),
                (
                    "owners",
                    models.ManyToManyField(related_name="owners", to=settings.AUTH_USER_MODEL, verbose_name="Owners"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.IntegerField(choices=[(1, "Member")], default=1)),
            ],
        ),
        migrations.CreateModel(
            name="TransactionType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("way", models.IntegerField(choices=[(1, "Income"), (2, "Outcome")])),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.IntegerField()),
                ("date", models.DateField()),
                ("description", models.TextField()),
                ("apartment", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="manager.apartment")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="manager.category")),
            ],
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
                ),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="manager.role")),
            ],
        ),
        migrations.CreateModel(
            name="Management",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("member", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="manager.member")),
            ],
        ),
    ]