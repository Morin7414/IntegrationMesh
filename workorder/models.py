from django.db import models
from datetime import datetime
from assets.models import EGM,SlotMachine
from inventory.models import InventoryItem
from django.contrib.auth.models import User
#from ckeditor.fields import RichTextField
from django.conf import settings


# Create your models here.
class WorkOrder (models.Model):
    STATUS_CHOICES = [
        ('TROUBLESHOOTING', 'TROUBLESHOOTING'),
        ('AWAITNG PARTS', 'AWAITNG PARTS'),
        ('NEEDS MEM CLEAR', 'NEEDS MEM CLEAR'),
        ('MONITORING', 'MONITORING'),
        ('REPAIRED', 'REPAIRED'),
    ]
    SERVICE_CHOICES = [
        ('IN SERVICE', 'IN SERVICE'),
        ('OUT OF SERVICE', 'OUT OF SERVICE'),     
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
    service_status = models.CharField(max_length=60, choices=SERVICE_CHOICES, default='IN SERVICE')
    maintenance_ticket = models.CharField(max_length=60, choices=STATUS_CHOICES, default='TROUBLESHOOTING')
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='Troubleshooting')
  
    date_created = models.DateTimeField(default=datetime.today)
    date_closed= models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   # type_of_repair =MultiSelectField(choices=REPAIR_CHOICES,max_length=255,blank=True, null =True)
    current_subject =models.CharField(max_length =255,blank = True, null =True)
  #  diagnostics = RichTextField(max_length =500,blank = True, null =True)
    diagnostics = models.TextField(max_length =500,blank = True, null =True)
    image = models.ImageField(upload_to='images/',blank=True,  null =True)
    asset_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255,  null=True, blank=True)
    model = models.CharField(max_length=255,  null=True, blank=True)
    central_office_remarks = models.CharField(max_length=255,  null=True, blank=True)
    slot_machine = models.ForeignKey(SlotMachine, on_delete=models.SET_NULL, null=True)

    def __str__(self):
       return f"Work Order # {self.id}  {self.slot_machine}"
 
class RepairLog(models.Model):
    image = models.ImageField(blank=True,  null =True)
    diagnostics = models.TextField(blank = True, null =True)
   # reason_for_repair = RichTextField(blank = True, null =True)
    reason_for_repair = models.TextField(max_length =500,blank = True, null =True)
    repair_log = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
    timestamp  = models.DateTimeField(default=datetime.today)
    user_stamp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length =255, blank = True, null =True)

    def __str__(self):
       return f"{self.status}"
    
class PartsRequired(models.Model):
    inventory = models.ForeignKey(InventoryItem,  on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    remarks = models.CharField(max_length=255)
    work_order = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
    price_extension = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
