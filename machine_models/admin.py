from django.contrib import admin
from .models import MachineModel
from django.urls import reverse

# Register your models here.
@admin.register(MachineModel)
class MachineModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_type', 'is_end_of_life']
    search_fields = ['model_name',]
    list_filter = ['is_end_of_life', 'machine_move_risk']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass the import URL to the template context
        extra_context['import_csv_url'] = reverse('machine_models:import_machine_data')  # Ensure this URL matches your URL pattern
        return super().changelist_view(request, extra_context=extra_context)


