from django.contrib import admin

from custom_admin.admin import custom_admin_site
from .models import  InventoryItem, PartsOrder

#class PartRequiredInline(admin.TabularInline):
   # model = PartRequired
   # extra = 0
   # raw_id_fields = ('inventory',)

class InventoryItemAdmin(admin.ModelAdmin):
     list_display = ('part_number',  'part_description')

class PartsOrderAdmin(admin.ModelAdmin):
    list_display = 'inventory','quantity', 'remarks'
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    raw_id_fields = ('inventory',)

#custom_admin_site.register(InventoryItem, InventoryItemAdmin) 
#custom_admin_site.register(PartsOrder, PartsOrderAdmin)
