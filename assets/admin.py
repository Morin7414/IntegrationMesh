from django.contrib import admin, messages
from .models import AssetTracker, SlotMachine, Model

from django.urls import reverse, path
from django.shortcuts import redirect
from django.conf import settings









class SlotMachineInline(admin.TabularInline):
    model = SlotMachine
    fk_name = 'machine_serial_number'  # Use if there's a ForeignKey relationship


class AssetTrackerAdmin(admin.ModelAdmin):
    list_display = ('machine_serial_number', 'slot_machine_name', 'slot_location', 'slot_game_name')
    search_fields = ('machine_serial_number', 'slot_machine_name', 'slot_location', 'slot_game_name')
    
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the URL for the import page to the context
        extra_context['import_serials_url'] = reverse('assets:import_serials')
        extra_context['sync_all_url'] = reverse('assets:sync_all_asset_trackers')
        return super().changelist_view(request, extra_context=extra_context)
    



class SlotMachineAdmin(admin.ModelAdmin):
    list_display = ('casino_id', 'slot_machine_name', 'slot_location', 'status')
    actions = ['delete_all_records']  # Add the custom action to actions list

    def delete_all_records(self, request, queryset):
        # Delete all SlotMachine records
        total_records = SlotMachine.objects.count()
        SlotMachine.objects.all().delete()
        self.message_user(request, f"All {total_records} SlotMachine records have been deleted.", level=messages.SUCCESS)
    delete_all_records.short_description = "Delete all SlotMachine records"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the namespaced URL for the upload page to the context
        extra_context['upload_csv_url'] = reverse('assets:slotmachine_upload_csv')
        return super().changelist_view(request, extra_context=extra_context)
    
class ModelAdmin(admin.ModelAdmin):
   # change_list_template = "admin/model_changelist.html"
    list_display = ('model_name' ,'manufacturer', 'model_type', 'machine_move_risk', 'current_amps')
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the import URL to the template context
        extra_context['import_csv_url'] = reverse('assets:import_machine_data')  # Ensure this URL matches your URL pattern
        return super().changelist_view(request, extra_context=extra_context)

 
admin.site.register(AssetTracker, AssetTrackerAdmin)
admin.site.register(SlotMachine, SlotMachineAdmin)
admin.site.register(Model, ModelAdmin)






