from django.contrib import admin
from .models import EGM
from import_export.admin import ImportExportModelAdmin

@admin.register(EGM)
class EGMAdmin(ImportExportModelAdmin, admin.ModelAdmin):
 #   list_display = ('asset_number','bank','game_theme','serial_number','model_name')
    list_display = ('asset_number', 'bank', 'game_theme', 'serial_number', 'model_name')
    search_fields = ['serial_number', 'asset_number']  # Add fields you want to search
 #   actions_on_top = False  # Remove actions dropdown from the top
  #  actions = None  # Disable the selection checkbox
   # raw_id_fields = ('model_name',) #add this for many to many









