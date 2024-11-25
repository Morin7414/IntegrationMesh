from django.db import models
from machine_models.models import MachineModel

# Create your models here.
class EGMSlotMachine(models.Model):  # Renamed from AssetTracker
    machine_serial_number = models.CharField(max_length=255, primary_key=True, unique=True, default="TEMP_SERIAL")
    slot_machine_name = models.CharField(max_length=100, blank=True, null=True)
    slot_location = models.CharField(max_length=100, blank=True, null=True)
    slot_game_name = models.CharField(max_length=100, blank=True, null=True)
    machine_model_name = models.CharField(max_length=100, blank=True, null=True)

    casino_id = models.CharField(max_length=100, blank=True, null=True)
    preventative_maintenance_date = models.DateField(null=True, blank=True, help_text="Date of the last preventative maintenance")

    def __str__(self):
        return f"{self.slot_machine_name} {self.casino_id} {self.machine_model_name}"