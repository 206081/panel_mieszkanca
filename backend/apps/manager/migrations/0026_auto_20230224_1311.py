# Generated by Django 3.2 on 2023-02-24 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0025_issue_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='apartment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.apartment'),
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('apartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.apartment')),
            ],
        ),
    ]