from django.db import models

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


#from workorder.models import WorkOrder
from django.core.exceptions import ValidationError


class InventoryItem(models.Model):
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=100)
    quantity = models.IntegerField( blank=True, null=True,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.part_number} {self.part_description}"
    


class PurchaseOrder(models.Model):
    items = models.ManyToManyField(InventoryItem, through='PurchaseOrderItem')
    vendor = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('received', 'Received')])

    def total_cost(self):
        return sum(item.total_cost() for item in self.purchaseorderitem_set.all())
    

@receiver(post_save, sender=PurchaseOrder)
def update_inventory_on_received(sender, instance, created, **kwargs):
    print(f"Sender: {sender.__name__}, Instance: {instance}, Created: {created}")
    if instance.status == 'received' and  created:
        print(f"Status: {instance.status}, Created: {created}")
        # Update inventory quantities for all items in the Purchase Order
        for order_item in instance.purchaseorderitem_set.all():
            order_item.item.quantity += order_item.quantity
            order_item.item.save()
   
    # Add more fields as needed

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_cost(self):
        return self.quantity * self.price

    # Add more fields as needed