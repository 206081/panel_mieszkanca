# Generated by Django 3.2 on 2023-02-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0039_apartment_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='summary',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='account',
            field=models.DecimalField(decimal_places=0, default=7594267874299032379588608, max_digits=26),
        ),
    ]
