# Generated by Django 3.2 on 2023-02-23 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0024_alter_issue_issue_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='description',
            field=models.TextField(default=''),
        ),
    ]