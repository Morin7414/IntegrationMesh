from django.contrib import admin
from .models import EGM
from workorder.models import  WorkOrder
from import_export.admin import ImportExportModelAdmin
#from custom_admin.admin import custom_admin_site

class WorkOrderInline(admin.TabularInline):
    model = WorkOrder
    list_display = ('maintenance_ticket','current_issue','central_office_remarks', 'date_created', 'date_closed', 'created_by',)
   # readonly_fields = ('price_extension',)
    extra = 1
  #  raw_id_fields = ('inventory',)


class EGMAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    
 #   list_display = ('asset_number','bank','game_theme','serial_number','model_name')
    list_display = ('asset_number', 'location', 'model')
    search_fields = ['asset_number', 'location', 'model']  # Add fields you want to search
    inlines = [WorkOrderInline]
    
 #   actions_on_top = False  # Remove actions dropdown from the top
  #  actions = None  # Disable the selection checkbox
   # raw_id_fields = ('model_name',) #add this for many to many


#custom_admin_site.register(EGM, EGMAdmin)

admin.site.register(EGM, EGMAdmin)







