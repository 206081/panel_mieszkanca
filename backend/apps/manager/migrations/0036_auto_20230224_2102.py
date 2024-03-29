# Generated by Django 3.2 on 2023-02-24 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0035_rename_is_paid_bill_is_balanced'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='store/pdfs/')),
            ],
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='manager.billtype'),
        ),
        migrations.CreateModel(
            name='HousingBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('bill_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='manager.billtype')),
            ],
        ),
    ]
