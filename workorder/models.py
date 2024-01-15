from django.db import models
from datetime import datetime
from assets.models import MachineMaster
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField




# Create your models here.
class WorkOrder (models.Model):
    STATUS_CHOICES = [
        ('In Service', 'In Service'),
        ('In Service - Awaiting Parts', 'In Service - Awaiting Parts'),
        ('Out of Service', 'Out of Service'),
        ('Diagnostic', 'Diagnostic'),
         ('Preventative Maintenance', 'Preventative Maintenance'),
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

    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='In Service')
    machine = models.ForeignKey(MachineMaster, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=datetime.today)
    date_closed= models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/',blank=True,  null =True)
   # type_of_repair =MultiSelectField(choices=REPAIR_CHOICES,max_length=255,blank=True, null =True)
    reason_for_repair =models.CharField(max_length =255, blank = True, null =True)

    def __str__(self):
       return self.image.url if self.image else ''
    
    def image_url(self):
        return self.image.url if self.image else ''
 

class RepairLog(models.Model):
    troubleshooting_and_repair = models.TextField()
    repair_log = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
    timestamp  = models.DateTimeField(default=datetime.today)
    user_stamp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
   