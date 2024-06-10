from django.contrib import admin
from .models import  InventoryItem,PurchaseOrder, PurchaseOrderItem

from django.http import HttpRequest
from .views import create_purchase_order 

#class InventoryItemAdmin(admin.ModelAdmin):
   #  list_display = ('part_number',  'part_description', 'price')



#admin.site.register(InventoryItem, InventoryItemAdmin) 


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1

class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseOrderItemInline]
    list_display = ['vendor', 'status', 'total_cost']
    list_filter = ['status']
    search_fields = ['vendor']
    actions = ['call_create_purchase_order_api'] 


    def call_create_purchase_order_api(self, request, queryset):
        print("HI")
        # Construct a POST request to your view function
        post_data = {
            'vendor': 'Test Vendor',
            'status': 'draft',
            'items': [
                {'item': 1, 'quantity': 10, 'price': 100},  # Adjust item ID and data as needed
            ]
        }
        request = HttpRequest()
        request.method = 'POST'
        request.POST = post_data

        # Call your view function with the constructed request
        response = create_purchase_order(request)
        
        # Redirect to the purchase order detail page or handle the response as needed
        return response
   
   




class InventoryItemAdmin(admin.ModelAdmin):
      list_display = ['part_number', 'part_description', 'quantity','price']
    


admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)