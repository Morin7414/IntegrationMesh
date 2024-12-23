from django.contrib import admin, messages
from .models import SlotMachine


from django.urls import reverse
from django.conf import settings



# Register your models here.
class SlotMachineAdmin(admin.ModelAdmin):
    list_display = ('slot_machine_name', 'slot_location', 'machine_serial_number', 'slot_game_name', 'machine_model_name', 'slot_denomination_value', 'last_updated', 'status')
    actions = ['delete_all_records']  # Add the custom action to actions list
    search_fields = ['slot_machine_name', 'machine_serial_number']  # Enable search functionality   

   

    def delete_all_records(self, request, queryset):
        # Delete all SlotMachine records
        total_records = SlotMachine.objects.count()
        SlotMachine.objects.all().delete()
        self.message_user(request, f"All {total_records} SlotMachine records have been deleted.", level=messages.SUCCESS)
    delete_all_records.short_description = "Delete all SlotMachine records"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the namespaced URL for the upload page to the context
        extra_context['upload_csv_url'] = reverse('slot_importer:slotmachine_upload_csv')
        return super().changelist_view(request, extra_context=extra_context)
    

 

admin.site.register(SlotMachine, SlotMachineAdmin)
