from django.db import models
from casinos.models import Casino
from datetime import datetime
from machine_models.models import MachineModel
# Create your models here.
class DepartmentalAsset(models.Model):  # Renamed from OperationalAsset
    casino = models.ForeignKey(Casino, on_delete=models.SET_NULL, null=True, related_name='departmental_assets')
    machine_name = models.CharField(max_length=100)
    machine_serial_number = models.CharField(max_length=255, primary_key=True, unique=True)
    machine_model_name = models.ForeignKey(MachineModel, to_field="model_name", on_delete=models.SET_NULL, null=True)
    machine_manufacturer_name1 = models.CharField(max_length=100, default='Unknown Manufacturer')
    last_updated = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=10, default='offline')

    def __str__(self):
        return f"{self.machine_name} ({self.machine_serial_number})"