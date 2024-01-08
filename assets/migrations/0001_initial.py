# Generated by Django 5.0 on 2024-01-08 04:26

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(max_length=100)),
                ('part_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('model_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('vendor', models.CharField(choices=[('Konami', 'Konami'), ('IGT', 'IGT'), ('Bally', 'Bally'), ('WMS', 'WMS'), ('Ainsworth', 'Ainsworth'), ('Aristocrat', 'Aristocrat'), ('Sci Games', 'Sci Games'), ('Everi', 'Everi'), ('Spielo', 'Spielo'), ('AGS', 'AGS'), ('Aruze', 'Aruze'), ('LnW', 'LnW'), ('Incredible Technologies', 'Incredible Technologies')], max_length=50)),
                ('machine_move_risk', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20)),
                ('cabinet_type', models.CharField(choices=[('Slant Video', 'Slant Video'), ('Upright Video', 'Upright Video')], max_length=20)),
                ('current_amps', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='MachineMaster',
            fields=[
                ('serial_number', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('asset_number', models.CharField(max_length=255)),
                ('game_theme', models.CharField(max_length=255)),
                ('date_PM', models.DateField(blank=True, null=True)),
                ('model_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='assets.model')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_service', 'In Service'), ('awaiting_parts', 'In Service - Awaiting Parts'), ('out_of_service', 'Out of Service')], default='in_service', max_length=20)),
                ('date_created', models.DateTimeField(default=datetime.date.today)),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.machinemaster')),
            ],
        ),
        migrations.CreateModel(
            name='RepairLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('troubleshooting_and_repair', models.TextField(default='Default Text')),
                ('time_spent', models.IntegerField(default=0)),
                ('repair_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.workorder')),
            ],
        ),
        migrations.CreateModel(
            name='PartRequired',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('comments', models.CharField(max_length=255)),
                ('inventory_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.inventoryitem')),
                ('part_required', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.workorder')),
            ],
        ),
    ]
