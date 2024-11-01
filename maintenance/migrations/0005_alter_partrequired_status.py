# Generated by Django 5.1.2 on 2024-10-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0004_alter_partrequired_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partrequired',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SITE_REQ', 'Site Requested'), ('CO_SENT', 'CO Sent'), ('CO_ORDERED', 'CO Ordered'), ('FULFILLED', 'Fulfilled')], default='PENDING', max_length=20),
        ),
    ]
