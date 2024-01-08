from django.contrib import admin
from .models import MachineMaster, Model, WorkOrder, InventoryItem, PartRequired, RepairLog


class PartRequiredInline(admin.StackedInline):
    model = PartRequired
    extra = 1
    raw_id_fields = ('inventory_item',)


class RepairLogInline(admin.StackedInline):
    model = RepairLog
    extra = 1

# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model_name','vendor','machine_move_risk','cabinet_type','current_amps')
    search_fields = [ 'model_name','vendor','machine_move_risk','cabinet_type','current_amps']
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None 

class MachineAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'asset_number', 'model_name', 'date_PM')
    search_fields = ['serial_number', 'asset_number']  # Add fields you want to search
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    raw_id_fields = ('model_name',) 

class InventoryItemAdmin(admin.ModelAdmin):
     list_display = ('part_number',  'part_description')
 


  
     

class WorkOrderAdmin(admin.ModelAdmin):
    inlines = [RepairLogInline,PartRequiredInline]
    list_display = ('status', 'machine')
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
   # inlines = [RepairLogInline]
 
    raw_id_fields = ('machine',)

    
  
admin.site.register(MachineMaster, MachineAdmin)
admin.site.register(Model,ModelAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin) 




