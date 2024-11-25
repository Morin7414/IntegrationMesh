from django.db import models

# Create your models here.
# Define the Casino model
class Casino(models.Model):
    casino_id = models.CharField(max_length=100, primary_key=True,unique=True)
    casino_name = models.CharField(max_length=255)
 #   casino_location = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='casino_logos/', null=True, blank=True)  # Logo of the casino

    def __str__(self):
        return self.casino_name

