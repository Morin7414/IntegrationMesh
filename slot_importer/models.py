from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from casinos.models import Casino
from machine_models.models import MachineModel
#from progressive.models import BankedProgressive, BEPS
 


class SlotMachine(models.Model):
    casino = models.ForeignKey(Casino, on_delete=models.SET_NULL, null=True, related_name='slot_machines_importer')  # Ensure 'Casino' is the correct model name
    slot_machine_name = models.CharField(max_length=100)
    slot_location = models.CharField(max_length=100)
    date_purchased = models.DateField(blank=True, null=True, help_text="Date when the model was introduced or purchased")
    machine_serial_number = models.CharField(max_length=255, primary_key=True, unique=True)
    slot_game_name = models.CharField(max_length=100)
    machine_model_name = models.ForeignKey(MachineModel, to_field="model_name", on_delete=models.SET_NULL, null=True, related_name='slot_machines_importer')  # Use a unique related_name
    slot_denomination_value = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=10, default='offline')

    banked_progressive = models.ForeignKey(
        'progressive.BankedProgressive',  # Lazy reference to avoid circular import
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="slot_machines_importer"
    )

    beps = models.ForeignKey(
        'progressive.BEPS',  # Lazy reference to avoid circular import
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="slot_machines_importer"
    )

    def __str__(self):
        return self.slot_machine_name