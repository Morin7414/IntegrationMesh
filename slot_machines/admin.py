from django.contrib import admin
from .models import EGMSlotMachine
from django.urls import reverse
# Register your models here.
@admin.register(EGMSlotMachine)
class SlotMachineAdmin(admin.ModelAdmin):
    list_display = ['slot_machine_name', 'machine_serial_number', 'slot_location', 'slot_game_name', 'casino_id', 'preventative_maintenance_date']
    search_fields = ['slot_machine_name', 'machine_serial_number', 'slot_game_name', 'casino_id']
    list_filter = [ 'casino_id', 'preventative_maintenance_date']

     
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the URL for the import page to the context
        extra_context['import_serials_url'] = reverse('slot_machines:import_serials')
        extra_context['sync_all_url'] = reverse('slot_machines:sync_all_asset_trackers')
        return super().changelist_view(request, extra_context=extra_context)

'''
class AssetTrackerAdmin(admin.ModelAdmin):
    list_display = (
        'machine_serial_number',
        'slot_machine_name',
        'slot_location',
        'slot_game_name',
        'machine_model_name',
    
        'preventative_maintenance_date',
    )
    list_filter = ( 'preventative_maintenance_date',)
    search_fields = ('slot_machine_name', 'slot_location', 'slot_game_name')


'''