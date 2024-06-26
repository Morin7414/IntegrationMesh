# Generated by Django 5.0.1 on 2024-06-10 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0007_alter_workorder_maintenance_ticket_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='maintenance_ticket',
            field=models.CharField(choices=[('TROUBLESHOOTING', 'TROUBLESHOOTING'), ('AWAITNG PARTS', 'AWAITNG PARTS'), ('NEEDS MEM CLEAR', 'NEEDS MEM CLEAR'), ('MONITORING', 'MONITORING'), ('REPAIRED', 'REPAIRED')], default='TROUBLESHOOTING', max_length=60),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('TROUBLESHOOTING', 'TROUBLESHOOTING'), ('AWAITNG PARTS', 'AWAITNG PARTS'), ('NEEDS MEM CLEAR', 'NEEDS MEM CLEAR'), ('MONITORING', 'MONITORING'), ('REPAIRED', 'REPAIRED')], default='Troubleshooting', max_length=60),
        ),
    ]
