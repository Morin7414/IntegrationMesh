from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from slot_importer.models import SlotMachine
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

PART_STATUS_CHOICES = [
    ('PENDING', 'Pending'),        
    ('SITE_REQ', 'Site Requested'),          # Part requested by the site
    ('CO_SENT', 'CO Sent'),                  # Central Office sent the part to the site
    ('CO_ORDERED', 'CO Ordered'),            # Central Office ordered the part (not in stock)
    ('FULFILLED', 'Fulfilled'),              # Request is complete, and site has received the part
]


# Define the SlotMachineMaintenanceForm model
class SlotMachineMaintenanceForm(models.Model):
    machine = models.ForeignKey(SlotMachine, on_delete=models.CASCADE,null=True, blank=True)
    issue_description = models.TextField( null=True, blank=True)
    operational_status = models.CharField(max_length=20, choices=OPERATIONAL_CHOICES, default='IN_SERVICE')
    maintenance_status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS_CHOICES, default='TROUBLESHOOTING')
    date_created = models.DateTimeField(default=timezone.now)
    completion_date = models.DateTimeField(null=True, blank=True, help_text="Date when maintenance was completed")
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

#    def __str__(self):
   #     machine_display = self.machine if self.machine else "Unknown Machine"
   #     return f"{machine_display} - {self.maintenance_status}"

   #return f"{self.machine} - {self.maintenance_status}"
    

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
    

class Kobetron(models.Model):
    slot_machine_maintenance_form = models.ForeignKey(
        'SlotMachineMaintenanceForm',
        on_delete=models.CASCADE,
        related_name='kobetron_records'
    )
    rom_position = models.CharField(max_length=50, help_text="Position of the ROM")
    program_number = models.CharField(max_length=50, help_text="Program number of the ROM")
    mfg_date = models.DateField(help_text="Manufacturing date of the ROM")
    kobetron_signature = models.CharField(max_length=50, help_text="Kobetron number")
    technician_signature = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technician_signatures',
        help_text="Technician who signed off"
    )
    security_reviewed = models.BooleanField(
        default=False,
        help_text="Indicates whether security has reviewed and approved this record"
    )
    security_review_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when security reviewed the record"
    )
    security_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kobetron_security_users',
        help_text="Security user who performed the review"
    )

    def __str__(self):
        return f"Kobetron Record for {self.slot_machine_maintenance_form}"



class LogicSeals(models.Model):
    casino_test_record = models.OneToOneField(
        SlotMachineMaintenanceForm,
        on_delete=models.CASCADE,
        related_name="logic_seals",
        blank=True,
        null=True
    )
    initial_seal_serial = models.CharField(max_length=20, blank=True, null=True, help_text="Serial number of the initial seal before accessing logic.")
    initial_seal_verified_by_security = models.BooleanField(default=False, help_text="Has the initial seal been verified by security?")
    initial_seal_verified_date = models.DateTimeField(blank=True, null=True, help_text="Date when the initial seal was verified by security.")
    initial_seal_verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="initial_seal_verified_users",
        help_text="Security user who verified the initial seal"
    )
    new_seal_serial = models.CharField(max_length=20, blank=True, null=True, help_text="Serial number of the new seal applied after work is completed.")
    new_seal_verified_by_security = models.BooleanField(default=False, help_text="Has the new seal been verified by security?")
    new_seal_verified_date = models.DateTimeField(blank=True, null=True, help_text="Date when the new seal was verified by security.")
    new_seal_verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="new_seal_verified_users",
        help_text="Security user who verified the new seal"
    )
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="logic_seal_technician", help_text="Technician who applied the new seal.")
    work_completed_date = models.DateTimeField(blank=True, null=True, help_text="Date when the technician completed their work and applied the new seal.")

    def __str__(self):
        return f"Logic Seals for {self.casino_test_record}"
