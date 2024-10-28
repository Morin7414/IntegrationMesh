from django.db import models

class InventoryItem(models.Model):
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=100)
    quantity = models.IntegerField( blank=True, null=True,default=0)
   # price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price per individual part")

    def __str__(self):
        return f"{self.part_number} {self.part_description}"