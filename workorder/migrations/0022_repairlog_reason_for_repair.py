# Generated by Django 5.0 on 2024-01-17 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0021_alter_workorder_reason_for_repair'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairlog',
            name='reason_for_repair',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
