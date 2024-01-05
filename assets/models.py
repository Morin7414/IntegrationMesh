from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Machine(models.Model):
    STATUS_CHOICES = [
        ('In Service', 'In Service'),
        ('Out of Service', 'Out of Service'),
        ('In Service, Awaiting Repair', 'In Service, Awaiting Repair'),
    ]
    assetNumber = models.CharField(max_length=100)
    serialNumber = models.CharField(max_length=100)
    gameTheme = models.CharField(max_length=100)
    modelID = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='In Service')

    def __str__(self):
        return f"{self.assetNumber} - Serial: {self.serialNumber} - Game Theme: {self.gameTheme} - Model: {self.modelID}"


class RepairLog(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='repair_logs')
    log_text = models.TextField()
    log_date = models.DateTimeField(default=timezone.now, editable=False)
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.machine.assetNumber} - Repair Log - {self.log_date} - Logged by: {self.logged_by.username if self.logged_by else 'N/A'}"