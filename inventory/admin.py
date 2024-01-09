from django.contrib import admin
from .models import  InventoryItem 

class InventoryItemAdmin(admin.ModelAdmin):
     list_display = ('part_number',  'part_description')

admin.site.register(InventoryItem, InventoryItemAdmin) 
