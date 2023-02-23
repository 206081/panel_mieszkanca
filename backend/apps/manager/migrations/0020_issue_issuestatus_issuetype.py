# Generated by Django 3.2 on 2023-02-23 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0019_apartment_interest'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('issue_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issue_status', to='manager.issuetype')),
                ('issue_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issue_type', to='manager.issuetype')),
            ],
        ),
    ]
