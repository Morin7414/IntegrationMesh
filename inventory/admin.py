from django.contrib import admin
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

admin.site.register(InventoryItem, InventoryItemAdmin) 
admin.site.register(PartsOrder, PartsOrderAdmin)
