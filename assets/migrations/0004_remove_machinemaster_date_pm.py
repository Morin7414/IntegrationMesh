# Generated by Django 5.0 on 2024-01-14 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_alter_machinemaster_model_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machinemaster',
            name='date_PM',
        ),
    ]