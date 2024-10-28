from django.contrib import admin
from .models import SlotMachineMaintenanceForm, TroubleshootingLog, Task, PartsUsed, PartsRequested

# Define the TroubleshootingLogInline for admin
class TroubleshootingLogInline(admin.TabularInline):
    model = TroubleshootingLog
    extra = 1  # Number of empty forms to display

# Define the TaskInline for admin
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

# Define the PartsUsedInline for admin
class PartsUsedInline(admin.TabularInline):
    model = PartsUsed
    extra = 1

# Define the PartsRequestedInline for admin
class PartsRequestedInline(admin.TabularInline):
    model = PartsRequested
    extra = 1

# Register the SlotMachineMaintenanceForm with all inlines
@admin.register(SlotMachineMaintenanceForm)
class SlotMachineMaintenanceFormAdmin(admin.ModelAdmin):
    list_display = ('machine', 'operational_status', 'maintenance_status', 'date_created', 'initiated_by')
    search_fields = ('machine__asset_number', 'maintenance_status', 'operational_status')
    list_filter = ('operational_status', 'maintenance_status', 'date_created')
    inlines = [TroubleshootingLogInline, TaskInline, PartsUsedInline, PartsRequestedInline]
