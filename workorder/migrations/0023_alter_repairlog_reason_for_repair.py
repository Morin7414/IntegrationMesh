# Generated by Django 5.0 on 2024-01-17 02:29

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0022_repairlog_reason_for_repair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairlog',
            name='reason_for_repair',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
