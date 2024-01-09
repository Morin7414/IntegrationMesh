from django.db import models

# Create your models here.
class InventoryItem(models.Model):
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=100)
    def __str__(self):
        return self.part_number
    