from django.db import models
from datetime import datetime
from assets.models import MachineMaster
from inventory.models import InventoryItem
from django.contrib.auth.models import User

# Create your models here.
class WorkOrder (models.Model):
    STATUS_CHOICES = [
        ('In Service', 'In Service'),
        ('In Service - Awaiting Parts', 'In Service - Awaiting Parts'),
        ('Out of Service', 'Out of Service'),
        ('Diagnostic', 'Diagnostic'),
         ('Preventative Maintenance', 'Preventative Maintenance'),



    ]
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='In Service')
    machine = models.ForeignKey(MachineMaster, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length =255, default='Default Title')
    date_created = models.DateTimeField(default=datetime.today)
    user_stamp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
       return f"WorkOrder {self.id} - {self.status} - {self.user_stamp}"
 
class PartRequired(models.Model):
    inventory = models.ForeignKey(InventoryItem,  on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    comments = models.CharField(max_length=255)
    part_required = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)

class RepairLog(models.Model):
    troubleshooting_and_repair = models.TextField()
    repair_log = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
    timestamp  = models.DateTimeField(default=datetime.today)
    user_stamp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
   