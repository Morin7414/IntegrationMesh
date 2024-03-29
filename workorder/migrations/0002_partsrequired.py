# Generated by Django 5.0.1 on 2024-03-04 05:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_delete_partsrequired'),
        ('workorder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartsRequired',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('remarks', models.CharField(max_length=255)),
                ('price_extension', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('inventory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.inventoryitem')),
                ('work_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workorder.workorder')),
            ],
        ),
    ]
