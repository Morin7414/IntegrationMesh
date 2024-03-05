from django.contrib import admin

from custom_admin.admin import custom_admin_site
from .models import  InventoryItem
#class PartRequiredInline(admin.TabularInline):
   # model = PartRequired
   # extra = 0
   # raw_id_fields = ('inventory',)

class InventoryItemAdmin(admin.ModelAdmin):
     list_display = ('part_number',  'part_description', 'price')



#custom_admin_site.register(InventoryItem, InventoryItemAdmin) 

admin.site.register(InventoryItem, InventoryItemAdmin) 