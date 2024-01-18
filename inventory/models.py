from django.db import models
from workorder.models import WorkOrder
from django.core.exceptions import ValidationError

class InventoryItem(models.Model):
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=100)
    quatity_available = models.IntegerField( blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.part_number} {self.part_description}"
    
class PartsOrder(models.Model):
    inventory = models.ForeignKey(InventoryItem,  on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    remarks = models.CharField(max_length=255)
    work_order = models.ForeignKey(WorkOrder,  on_delete=models.SET_NULL, null=True)
    price_extension = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Additional validation: Check if the ordered quantity is greater than available quantity
        if self.inventory and self.quantity > self.inventory.quantity_available:
            raise ValidationError("Ordered quantity exceeds available quantity in inventory.")
        
        super().save(*args, **kwargs)
    