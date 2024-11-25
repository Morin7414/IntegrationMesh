# Generated by Django 5.1.2 on 2024-11-25 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MachineModel',
            fields=[
                ('model_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True)),
                ('model_type', models.CharField(blank=True, max_length=255, null=True)),
                ('machine_move_risk', models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], help_text='Risk associated with moving this machine', max_length=20, null=True)),
                ('current_amps', models.FloatField(blank=True, help_text='Current (in amps) required by the machine', null=True)),
                ('is_depreciated', models.BooleanField(default=False, help_text='Indicates if the model is depreciated')),
                ('depreciated_since', models.DateField(blank=True, help_text='Date when the model was marked as depreciated', null=True)),
                ('dimensions', models.JSONField(blank=True, help_text="Cabinet dimensions as {'height': , 'width': , 'depth': }", null=True)),
                ('weight', models.FloatField(blank=True, help_text='Weight of the machine in lb', null=True)),
                ('screen_size', models.FloatField(blank=True, help_text='Screen size in inches', null=True)),
                ('model_image', models.ImageField(blank=True, help_text='Image of the model', null=True, upload_to='model_pics/')),
            ],
            options={
                'verbose_name': 'Slot Machine Model',
                'verbose_name_plural': 'Slot Machine Models',
            },
        ),
    ]
