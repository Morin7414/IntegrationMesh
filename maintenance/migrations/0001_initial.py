# Generated by Django 5.1.2 on 2024-10-28 00:36

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0005_assettracker_machine_model_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SlotMachineMaintenanceForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_description', models.TextField(blank=True, null=True)),
                ('operational_status', models.CharField(choices=[('IN_SERVICE', 'In Service'), ('OUT_OF_SERVICE', 'Out of Service')], default='IN_SERVICE', max_length=20)),
                ('maintenance_status', models.CharField(choices=[('TROUBLESHOOTING', 'Troubleshooting'), ('AWAITING_PARTS', 'Awaiting Parts'), ('NEEDS_MEM_CLEAR', 'Needs Mem Clear'), ('CONVERSION', 'Conversion'), ('INSTALL', 'Install'), ('MONITORING', 'Monitoring'), ('REPAIRED', 'Repaired')], default='TROUBLESHOOTING', max_length=20)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('completion_date', models.DateTimeField(blank=True, help_text='Date when maintenance was completed', null=True)),
                ('initiated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.assettracker')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='Description of the suggested task')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='PENDING', help_text='Current status of the task', max_length=20)),
                ('date_assigned', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time when the task was assigned')),
                ('date_completed', models.DateTimeField(blank=True, help_text='Date and time when the task was completed', null=True)),
                ('assigned_by', models.ForeignKey(blank=True, help_text='User who assigned the task', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_by_tasks', to=settings.AUTH_USER_MODEL)),
                ('assigned_to', models.ForeignKey(blank=True, help_text='Support worker assigned to the task', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
                ('maintenance_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='maintenance.slotmachinemaintenanceform')),
            ],
        ),
        migrations.CreateModel(
            name='TroubleshootingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('narrative', models.TextField(blank=True, help_text='Enter actions taken, outcome, and additional brief details', null=True)),
                ('time_spent', models.DurationField(help_text='Time spent on troubleshooting')),
                ('date_performed', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time of troubleshooting action')),
                ('maintenance_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='troubleshooting_logs', to='maintenance.slotmachinemaintenanceform')),
                ('performed_by', models.ForeignKey(blank=True, help_text='User who performed the troubleshooting', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
