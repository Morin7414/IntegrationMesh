from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from assets.models import AssetTracker
from inventory.models import  InventoryItem

# Create your models here.
# Define choices for operational and maintenance statuses
OPERATIONAL_CHOICES = [
    ('IN_SERVICE', 'In Service'),
    ('OUT_OF_SERVICE', 'Out of Service'),
]

MAINTENANCE_STATUS_CHOICES = [
    ('TROUBLESHOOTING', 'Troubleshooting'),
    ('AWAITING_PARTS', 'Awaiting Parts'),
    ('NEEDS_MEM_CLEAR', 'Needs Mem Clear'),
    ('CONVERSION', 'Conversion'),
    ('INSTALL', 'Install'),
    ('MONITORING', 'Monitoring'),
    ('REPAIRED', 'Repaired'),
]

TASK_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('IN_PROGRESS', 'In Progress'),
    ('COMPLETED', 'Completed'),
]


# Define the SlotMachineMaintenanceForm model
class SlotMachineMaintenanceForm(models.Model):
    machine = models.ForeignKey(AssetTracker, on_delete=models.CASCADE)
    issue_description = models.TextField( null=True, blank=True)
    operational_status = models.CharField(max_length=20, choices=OPERATIONAL_CHOICES, default='IN_SERVICE')
    maintenance_status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS_CHOICES, default='TROUBLESHOOTING')
    date_created = models.DateTimeField(default=timezone.now)
    completion_date = models.DateTimeField(null=True, blank=True, help_text="Date when maintenance was completed")
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.machine} - {self.maintenance_status}"
    

# Define the TroubleshootingLog model
class TroubleshootingLog(models.Model):
    maintenance_form = models.ForeignKey(SlotMachineMaintenanceForm, on_delete=models.CASCADE, related_name="troubleshooting_logs")
    narrative = models.TextField(null=True, blank=True, help_text="Enter actions taken, outcome, and additional brief details")
    time_spent = models.DurationField(help_text="Time spent on troubleshooting")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="User who performed the troubleshooting")
    date_performed = models.DateTimeField(default=timezone.now, help_text="Date and time of troubleshooting action")

    def __str__(self):
        return f"{self.maintenance_form} - {self.action[:20]}"
    
# Define the Task model
class Task(models.Model):
    maintenance_form = models.ForeignKey(SlotMachineMaintenanceForm, on_delete=models.CASCADE, related_name="tasks")
    description = models.TextField(help_text="Description of the suggested task")
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_by_tasks", help_text="User who assigned the task")
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='PENDING', help_text="Current status of the task")
    date_assigned = models.DateTimeField(default=timezone.now, help_text="Date and time when the task was assigned")
    date_completed = models.DateTimeField(null=True, blank=True, help_text="Date and time when the task was completed")

    def __str__(self):
        return f"Task for {self.maintenance_form} - {self.status}"
    

PART_STATUS_CHOICES = [
    ('PENDING', 'Pending'),        
    ('SITE_REQ', 'Site Requested'),          # Part requested by the site
    ('CO_SENT', 'CO Sent'),                  # Central Office sent the part to the site
    ('CO_ORDERED', 'CO Ordered'),            # Central Office ordered the part (not in stock)
    ('FULFILLED', 'Fulfilled'),              # Request is complete, and site has received the part
]

# Unified PartRequired model
class PartRequired(models.Model):
    maintenance_form = models.ForeignKey('SlotMachineMaintenanceForm', on_delete=models.CASCADE, related_name="parts_required")
    part = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price per individual part")
    quantity = models.PositiveIntegerField(default=1)
    date_requested = models.DateTimeField(default=timezone.now, help_text="Date when the part was requested")
    date_fulfilled = models.DateTimeField(null=True, blank=True, help_text="Date when the part request was fulfilled")
    status = models.CharField(max_length=20, choices=PART_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.part} - {self.status} in {self.maintenance_form}"