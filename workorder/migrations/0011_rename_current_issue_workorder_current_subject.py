# Generated by Django 5.0.1 on 2024-06-12 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0010_workorder_machine'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='current_issue',
            new_name='current_subject',
        ),
    ]
