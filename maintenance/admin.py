from django.contrib import admin
from .models import (
    SlotMachineMaintenanceForm, 
    TroubleshootingLog, 
    Task, 
   # PartRequired, 
    Kobetron, 
 #   CasinoTestRecord, 
 #   SoftGMUAfter,
 #   SoftGMUBefore,
 #   Progressive, 
 #   BetWin, 
 ##   TestSettings,
    LogicSeals
)

# Inline for TroubleshootingLog within SlotMachineMaintenanceForm
class TroubleshootingLogInline(admin.TabularInline):
    model = TroubleshootingLog
    extra = 0

# Inline for Task within SlotMachineMaintenanceForm
class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

# Inline for PartRequired within SlotMachineMaintenanceForm
#class PartRequiredInline(admin.TabularInline):
 #   model = PartRequired
  #  extra = 0

# Inline for Kobetron within SlotMachineMaintenanceForm
class KobetronInline(admin.TabularInline):
    model = Kobetron
    extra = 0


class LogicSealsInline(admin.StackedInline):
    model = LogicSeals
    extra = 0
    readonly_fields = ('initial_seal_verified_date', 'new_seal_verified_date', 'work_completed_date')
  


# Admin for SlotMachineMaintenanceForm with inlines
@admin.register(SlotMachineMaintenanceForm)
class SlotMachineMaintenanceFormAdmin(admin.ModelAdmin):
    list_display = ('machine', 'operational_status', 'maintenance_status', 'date_created', 'completion_date', 'initiated_by')
    search_fields = ('machine__asset_number', 'maintenance_status', 'operational_status')
    list_filter = ('operational_status', 'maintenance_status', 'date_created')
    inlines = [TroubleshootingLogInline, TaskInline, LogicSealsInline,KobetronInline, ]
    raw_id_fields = ('machine',)
'''
# Admin for CasinoTestRecord
@admin.register(CasinoTestRecord)
class CasinoTestRecordAdmin(admin.ModelAdmin):
    list_display = ('maintenance_form',)
    inlines = [SoftGMUBeforeInline,SoftGMUAfterInline,TestSettingsInline,  ProgressiveInline, BetWinInline,]
'''