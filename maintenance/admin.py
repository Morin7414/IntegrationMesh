from django.contrib import admin
from .models import SlotMachineMaintenanceForm, TroubleshootingLog, Task, PartRequired

class TroubleshootingLogInline(admin.TabularInline):
    model = TroubleshootingLog
    extra = 1
    fields = ('narrative', 'time_spent', 'performed_by', 'date_performed')
    readonly_fields = ('date_performed',)

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ('description', 'assigned_by', 'status', 'date_assigned', 'date_completed')
    readonly_fields = ('date_assigned',)

class PartRequiredInline(admin.TabularInline):
    model = PartRequired
    extra = 1
    fields = ('part', 'quantity', 'price_per_unit', 'status', 'date_requested', 'date_fulfilled')
    readonly_fields = ('date_requested',)

@admin.register(SlotMachineMaintenanceForm)
class SlotMachineMaintenanceFormAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_status', 'operational_status', 'date_created', 'completion_date', 'initiated_by')
    list_filter = ('maintenance_status', 'operational_status', 'date_created')
    search_fields = ('machine__asset_number', 'issue_description')
    date_hierarchy = 'date_created'
    inlines = [TroubleshootingLogInline, TaskInline, PartRequiredInline]
    fieldsets = (
        (None, {
            'fields': ('machine', 'issue_description', 'operational_status', 'maintenance_status', 'initiated_by')
        }),
        ('Dates', {
            'fields': ('date_created', 'completion_date'),
        }),
    )
    readonly_fields = ('date_created',)

@admin.register(TroubleshootingLog)
class TroubleshootingLogAdmin(admin.ModelAdmin):
    list_display = ('maintenance_form', 'performed_by', 'time_spent', 'date_performed')
    list_filter = ('date_performed',)
    search_fields = ('maintenance_form__machine__asset_number', 'narrative')
    date_hierarchy = 'date_performed'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('maintenance_form', 'description', 'status', 'assigned_by', 'date_assigned', 'date_completed')
    list_filter = ('status', 'date_assigned')
    search_fields = ('maintenance_form__machine__asset_number', 'description')
    date_hierarchy = 'date_assigned'

@admin.register(PartRequired)
class PartRequiredAdmin(admin.ModelAdmin):
    list_display = ('maintenance_form', 'part', 'quantity', 'price_per_unit', 'status', 'date_requested', 'date_fulfilled')
    list_filter = ('status', 'date_requested')
    search_fields = ('maintenance_form__machine__asset_number', 'part__name')
    date_hierarchy = 'date_requested'