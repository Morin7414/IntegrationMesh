from django.db import models
from datetime import datetime
from assets.models import EGM
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.conf import settings






# Create your models here.
class WorkOrder (models.Model):
    STATUS_CHOICES = [
        ('MACHINE TROUBLESHOOTING', 'TROUBLESHOOTING'),
        ('MACHINE DOWN - AWAITNG PARTS', 'MACHINE DOWN - AWAITNG PARTS'),
        ('MACHINE IN SERVICE - AWAITNG PARTS', 'MACHINE IN SERVICE - AWAITNG PARTS'),
        ('REPAIR COMPLETED', 'REPAIR COMPLETED'),
    ]

    REPAIR_CHOICES = (
    ('Lock Repairs', 'Lock Repairs'),
    ('Door/Latch Repair', 'Door/Latch Repair'),
    ('Player Interface Repairs', 'Player Interface Repairs'),
    ('Bill Validator Repairs', 'Bill Validator Repairs'),
    ('Ticket Printer Repairs', 'Ticket Printer Repairs'),
    ('Card Reader Repairs', 'Card Reader Repairs'),
    ('Electrical Component Repairs', 'Electrical Component Repairs'),
    ('Display/Mechanical Reel Repairs', 'Display/Mechanical Reel Repairs'),
    ('Software Troubleshooting', 'Software Troubleshooting'),
    ('Sound System Repairs', 'Sound System Repairs'),
    ('Cabinet Repairs', 'Cabinet Repairs'),
    ('Network and Communication Repairs', 'Network and Communication Repairs'),
    ('Power Supply Repairs', 'Power Supply Repairs'),
    ('Cabinet Lighting Repairs', 'Cabinet Lighting Repairs'),
    ('Internal Cleaning and Dust Removal', 'Internal Cleaning and Dust Removal'),
    ('Firmware Updates', 'Firmware Updates'),
    ('CPU Repairs', 'CPU Repairs'),
    ('Backplane Repairs', 'Backplane Repairs'),
)

    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='Troubleshooting')
    machine = models.ForeignKey(EGM, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=datetime.today)
    date_closed= models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   # type_of_repair =MultiSelectField(choices=REPAIR_CHOICES,max_length=255,blank=True, null =True)
    reason_for_repair =models.CharField(max_length =255,blank = True, null =True)
    diagnostics = RichTextField(max_length =500,blank = True, null =True)
    image = models.ImageField(upload_to='images/',blank=True,  null =True)

    asset_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255,  null=True, blank=True)
    model = models.CharField(max_length=255,  null=True, blank=True)
    recent_update = models.CharField(max_length=255,  null=True, blank=True)

 
    def __str__(self):
       return f"Work Order # {self.id}  {self.machine}"
 

class RepairLog(models.Model):
    image = models.ImageField(blank=True,  null =True)
    diagnostics = models.TextField(blank = True, null =True)
    reason_for_repair = RichTextField(blank = True, null =True)
    repair_log = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
    timestamp  = models.DateTimeField(default=datetime.today)
    user_stamp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length =255, blank = True, null =True)

    def __str__(self):
       return f"{self.status}"
    
