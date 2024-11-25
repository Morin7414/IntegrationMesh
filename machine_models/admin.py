from django.contrib import admin
from .models import MachineModel
from django.urls import reverse

# Register your models here.
@admin.register(MachineModel)
class MachineModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'manufacturer', 'model_type', 'is_depreciated']
    search_fields = ['model_name', 'manufacturer']
    list_filter = ['is_depreciated', 'machine_move_risk']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the import URL to the template context
        extra_context['import_csv_url'] = reverse('machine_models:import_machine_data')  # Ensure this URL matches your URL pattern
        return super().changelist_view(request, extra_context=extra_context)


'''
class ModelAdmin(admin.ModelAdmin):
   # change_list_template = "admin/model_changelist.html"
    list_display = (
        'model_name',
        'manufacturer',
        'model_type',
        'machine_move_risk',
        'current_amps',
        'is_depreciated',
        'depreciated_since',
        'weight',
        'screen_size',
    )
    list_filter = ('machine_move_risk', 'is_depreciated', 'depreciated_since')
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the import URL to the template context
        extra_context['import_csv_url'] = reverse('assets:import_machine_data')  # Ensure this URL matches your URL pattern
        return super().changelist_view(request, extra_context=extra_context)

'''