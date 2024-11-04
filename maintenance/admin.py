from django.contrib import admin
from .models import (
    SlotMachineMaintenanceForm, 
    TroubleshootingLog, 
    Task, 
    PartRequired, 
    Kobetron, 
    CasinoTestRecord, 
    SoftGMUAfter,
    SoftGMUBefore,
    Progressive, 
    BetWin, 
    TestSettings,
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
class PartRequiredInline(admin.TabularInline):
    model = PartRequired
    extra = 0

# Inline for Kobetron within SlotMachineMaintenanceForm
class KobetronInline(admin.TabularInline):
    model = Kobetron
    extra = 0

# Inline for CasinoTestRecord within SlotMachineMaintenanceForm
class CasinoTestRecordInline(admin.TabularInline):
    model = CasinoTestRecord
    extra = 0
 


class SoftGMUBeforeInline(admin.StackedInline):
    model = SoftGMUBefore
    extra = 1

class SoftGMUAfterInline(admin.StackedInline):
    model = SoftGMUAfter
    extra = 1
   
   

class ProgressiveInline(admin.TabularInline):
    model = Progressive
    extra = 1

class BetWinInline(admin.TabularInline):
    model = BetWin
    extra = 1

class TestSettingsInline(admin.TabularInline):
    model = TestSettings
    extra = 1


class LogicSealsInline(admin.StackedInline):
    model = LogicSeals
    extra = 0
    readonly_fields = ('initial_seal_verified_date', 'new_seal_verified_date', 'work_completed_date')
    fieldsets = (
        (None, {
            'fields': ('casino_test_record',)
        }),
        ('Initial Seal Verification', {
            'fields': (
                'initial_seal_serial',
                'initial_seal_verified_by_security',
                'initial_seal_verified_date'
            ),
            'description': 'Security must verify the initial seal before technician access.'
        }),
        ('New Seal Application and Verification', {
            'fields': (
                'technician',
                'work_completed_date',
                'new_seal_serial',
                'new_seal_verified_by_security',
                'new_seal_verified_date'
            ),
            'description': 'After work is completed, a new seal is applied and verified by security.'
        }),
    )


# Admin for SlotMachineMaintenanceForm with inlines
@admin.register(SlotMachineMaintenanceForm)
class SlotMachineMaintenanceFormAdmin(admin.ModelAdmin):
    list_display = ('machine', 'operational_status', 'maintenance_status', 'date_created', 'completion_date', 'initiated_by')
    search_fields = ('machine__asset_number', 'maintenance_status', 'operational_status')
    list_filter = ('operational_status', 'maintenance_status', 'date_created')
    inlines = [TroubleshootingLogInline, TaskInline, CasinoTestRecordInline,PartRequiredInline, LogicSealsInline,KobetronInline, ]

# Admin for CasinoTestRecord
@admin.register(CasinoTestRecord)
class CasinoTestRecordAdmin(admin.ModelAdmin):
    list_display = ('maintenance_form',)
    inlines = [SoftGMUBeforeInline,SoftGMUAfterInline,TestSettingsInline,  ProgressiveInline, BetWinInline,]