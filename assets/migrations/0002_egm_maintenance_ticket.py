# Generated by Django 5.0.1 on 2024-06-11 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
        ('workorder', '0009_remove_workorder_machine'),
    ]

    operations = [
        migrations.AddField(
            model_name='egm',
            name='maintenance_ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workorder.workorder'),
        ),
    ]
