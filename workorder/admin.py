from django.contrib import admin
from .models import  WorkOrder
from .models import PartRequired, RepairLog
from django import forms
from django.utils import timezone


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
       # exclude = ['user_stamp', 'date_created']  # Exclude the user_stamp field from the form
        fields = '__all__'

    
    
class RepairLogForm(forms.ModelForm):
    class Meta:
        model = RepairLog
        exclude = ['user_stamp', 'date_created']  
        fields = '__all__'

        
### INLINES############################################################################################################################################
class PartRequiredInline(admin.TabularInline):
    model = PartRequired
    extra = 0
    raw_id_fields = ('inventory',)


class RepairLogInline(admin.TabularInline):
    model = RepairLog
    readonly_fields = ('timestamp', 'user_stamp')
    extra = 0


    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing records
    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting existing records
    
  
  
    def save_model(self, request, obj, form, change):
        # Set the userstamp to the current logged-in user
       
        if request.user.is_authenticated:
            obj.user_stamp = request.user
            obj.timestamp = timezone.now()
        obj.save()
        # Set the timestamp to the current time
   

    
### ADMIN    
   
class WorkOrderAdmin(admin.ModelAdmin):
    form = WorkOrderForm
    inlines = [RepairLogInline,PartRequiredInline]
    list_display = ('status', 'user_stamp', 'date_created')
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    raw_id_fields = ('machine',)
    readonly_fields = ('date_created', 'user_stamp')
    
    def save_model(self, request, obj, form, change):
        if not obj.id:
            print("Hi")
            obj.user_stamp = request.user
            obj.date_created = timezone.now()
      
        obj.save()

  



class RepairLogAdmin(admin.ModelAdmin):
    form = RepairLogForm
    list_display = ('repair_log', 'troubleshooting_and_repair',  'timestamp','user_stamp')
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox

    def save_model(self, request, obj, form, change):
        if not obj.id:
            print("Hi")
            obj.user_stamp = request.user
        obj.save()
    




class PartRequiredAdmin(admin.ModelAdmin):
    list_display = 'inventory','quantity', 'comments'
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    raw_id_fields = ('inventory',)
    
admin.site.register(WorkOrder,  WorkOrderAdmin)
admin.site.register(RepairLog, RepairLogAdmin)
admin.site.register(PartRequired, PartRequiredAdmin)