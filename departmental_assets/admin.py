from django.contrib import admin
from .models import DepartmentalAsset  # Updated model name
from django.urls import reverse

# Register your models here.
@admin.register(DepartmentalAsset)
class DepartmentalAssetAdmin(admin.ModelAdmin):
    list_display = ['machine_name', 'machine_serial_number', 'casino', 'status', 'last_updated']
    search_fields = ['machine_name', 'machine_serial_number', 'casino__casino_name']
    list_filter = ['status', 'casino']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['upload_csv_url'] = reverse('departmental_assets:import_operational_assets')
        return super().changelist_view(request, extra_context=extra_context)



"""
@admin.register(OperationalAsset)
class OperationalAssetAdmin(admin.ModelAdmin):
    list_display = ( 'machine_name', 'machine_serial_number', 'machine_model_name', 'machine_manufacturer_name1', 'last_updated', 'status')  # Fields to display in the admin list view
    search_fields = ('machine_name', 'machine_serial_number')  # Fields to enable search functionality
    list_filter = ('status', 'last_updated')  # Fields to filter by in the admin sidebar
    ordering = ('machine_name',)  # Default ordering in the admin list view
    readonly_fields = ('last_updated',)  # Fields set as read-only

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['upload_csv_url'] = reverse('assets:import_operational_assets')
        return super().changelist_view(request, extra_context=extra_context)
"""