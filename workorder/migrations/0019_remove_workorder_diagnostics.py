# Generated by Django 5.0 on 2024-01-16 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0018_remove_repairlog_diagnostic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workorder',
            name='diagnostics',
        ),
    ]