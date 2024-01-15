from django.contrib import admin
from .models import MachineMaster, Model

# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model_name','vendor','machine_move_risk','cabinet_type','current_amps')
    search_fields = [ 'model_name','vendor','machine_move_risk','cabinet_type','current_amps']
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None 

class MachineAdmin(admin.ModelAdmin):
    list_display = ('asset_number','game_theme','serial_number','model_name')
    search_fields = ['serial_number', 'asset_number']  # Add fields you want to search
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
   # raw_id_fields = ('model_name',) #add this for many to many

admin.site.register(MachineMaster, MachineAdmin)
#admin.site.register(Model,ModelAdmin)






