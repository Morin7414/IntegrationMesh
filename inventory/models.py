from django.db import models
from workorder.models import WorkOrder

class InventoryItem(models.Model):
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=100)
    quatity_available = models.IntegerField( blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return self.part_number
    
class PartsOrder(models.Model):
    inventory = models.ForeignKey(InventoryItem,  on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    remarks = models.CharField(max_length=255)
    work_order = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
    price_extension = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    