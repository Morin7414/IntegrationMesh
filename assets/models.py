from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class Model(models.Model):
    MOVE_RISK_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    model_name = models.CharField(max_length=255, primary_key=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    model_type = models.CharField(max_length=255, blank=True, null=True)
    machine_move_risk = models.CharField(max_length=20, choices=MOVE_RISK_CHOICES, blank=True, null=True, help_text="Risk associated with moving this machine")
    current_amps = models.FloatField(blank=True, null=True, help_text="Current (in amps) required by the machine")
    is_depreciated = models.BooleanField(default=False, help_text="Indicates if the model is depreciated")
    depreciated_since = models.DateField(blank=True, null=True, help_text="Date when the model was marked as depreciated")
    dimensions = models.JSONField(blank=True, null=True, help_text="Cabinet dimensions as {'height': , 'width': , 'depth': }")
    weight = models.FloatField(blank=True, null=True, help_text="Weight of the machine in lb")
    screen_size = models.FloatField(blank=True, null=True, help_text="Screen size in inches")
    model_image = models.ImageField(upload_to='model_pics/', blank=True, null=True, help_text="Image of the model")

    def __str__(self):
        return f"{self.model_name} - {self.model_type or 'Unknown Type'}"

    def get_dimension_str(self):
        if self.dimensions:
            return f"{self.dimensions.get('height', 'N/A')} x {self.dimensions.get('width', 'N/A')} x {self.dimensions.get('depth', 'N/A')} cm"
        return "Dimensions not specified"

    class Meta:
        verbose_name = "Slot Machine Model"
        verbose_name_plural = "Slot Machine Models"

class AssetTracker(models.Model):
   # id = models.AutoField(primary_key=True)
    machine_serial_number = models.CharField(max_length=255, primary_key=True, unique =True, default="TEMP_SERIAL")
    slot_machine_name = models.CharField(max_length=100, blank=True, null=True)
    slot_location = models.CharField(max_length=100, blank=True, null=True)
    slot_game_name = models.CharField(max_length=100, blank=True, null=True)  # New field
    machine_model_name = models.CharField(max_length=100, blank=True, null=True)  # New field for model name
    casino_id = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return f"Asset Tracker: {self.machine_serial_number}"
    
    def sync_with_slot_machine(self):
        # Sync data from SlotMachine model
        slot_machine = SlotMachine.objects.filter(machine_serial_number=self.machine_serial_number).first()
        if slot_machine:
            self.slot_machine_name = slot_machine.slot_machine_name
            self.slot_location = slot_machine.slot_location
            self.slot_game_name = slot_machine.slot_game_name  # Sync slot_game_name
            self.machine_model_name = slot_machine.machine_model_name.model_name if slot_machine.machine_model_name else None  # Sync machine_model_name
            self.save()


class SlotMachine(models.Model):
    casino_id = models.CharField(max_length=100)
    slot_machine_name = models.CharField(max_length=100)
    slot_location = models.CharField(max_length=100)
    slot_cabinet_name = models.CharField(max_length=100)
    textbox34 = models.CharField(max_length=100)
    machine_serial_number = models.CharField(max_length=255, primary_key=True, unique =True)
    slot_game_name = models.CharField(max_length=100)
    machine_model_name = models.ForeignKey(Model, to_field="model_name", on_delete=models.SET_NULL, null=True)
    machine_manufacturer_name1 = models.CharField(max_length=100,default='Unknown Manufacturer')  # Ensure this name matches
    slot_denomination = models.CharField(max_length=100)
    slot_denomination_value = models.CharField(max_length=100)
    textbox46 = models.CharField(max_length=100)
    gaming_day_count = models.IntegerField(null=True, blank = True)
    last_updated = models.DateTimeField(default=datetime.now)  # New field for last updated date
    status = models.CharField(max_length=10, default='offline')  # New field for status

    def __str__(self):
        return self.slot_machine_name

  






  
    