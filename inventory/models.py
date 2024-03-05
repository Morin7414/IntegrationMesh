from django.db import models
#from workorder.models import WorkOrder
from django.core.exceptions import ValidationError

class InventoryItem(models.Model):
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=100)
    #quatity_available = models.IntegerField( blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.part_number} {self.part_description}"