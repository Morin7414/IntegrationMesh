# Generated by Django 5.0 on 2024-01-14 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0009_rename_user_stamp_workorder_created_by'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PartRequired',
        ),
    ]