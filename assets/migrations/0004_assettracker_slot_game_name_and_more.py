# Generated by Django 5.1.2 on 2024-10-27 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_alter_model_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assettracker',
            name='slot_game_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assettracker',
            name='slot_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assettracker',
            name='slot_machine_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
