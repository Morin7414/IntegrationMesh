from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Model(models.Model): 
    MOVE_RISK_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    model_name = models.CharField(max_length=255,primary_key=True)
    manufacturer = models.CharField(max_length=255, blank = True, null =True)
    model_type = models.CharField(max_length=255, blank = True, null =True)
    machine_move_risk = models.CharField(max_length=20, choices=MOVE_RISK_CHOICES, blank = True, null =True)
    current_amps = models.FloatField(blank=True, null=True)
    model_image = models.ImageField(upload_to='model_pics/',blank=True,  null =True)



    def __str__(self):
        return self.model_name

class EGM(models.Model):
   # id = models.AutoField(primary_key=True)
    asset_number = models.CharField(max_length=100, blank = True, null =True)
    location = models.CharField(max_length=100, blank = True, null =True)
    model = models.CharField(max_length=100, blank = True, null =True)
   # maintenance_ticket = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
   # def __str__(self):
    #    return self.asset_number
#
 
    def __str__(self):
        return f"{self.asset_number}    {self.location}  {self.model}"

class SlotMachine(models.Model):
    casino_id = models.CharField(max_length=100)
    slot_machine_name = models.CharField(max_length=100)
    slot_location = models.CharField(max_length=100)
    slot_cabinet_name = models.CharField(max_length=100)
    textbox34 = models.CharField(max_length=100)
    machine_serial_number = models.CharField(max_length=255, primary_key=True, unique =True)
    slot_game_name = models.CharField(max_length=100)
    machine_model_name = models.ForeignKey(Model, to_field='model_name', on_delete=models.CASCADE, related_name='slot_machines')
    machine_manufacturer_name1 = models.CharField(max_length=100,default='Unknown Manufacturer')  # Ensure this name matches
    slot_denomination = models.CharField(max_length=100)
    slot_denomination_value = models.FloatField()
    textbox46 = models.CharField(max_length=100)
    gaming_day_count = models.IntegerField()
    last_updated = models.DateTimeField(default=datetime.now)  # New field for last updated date
    status = models.CharField(max_length=10, default='offline')  # New field for status

    def __str__(self):
        return self.slot_machine_name

  






  
    