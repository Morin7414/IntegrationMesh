from django.contrib import admin
from .models import  WorkOrder
from .models import  RepairLog
from django import forms
from django.utils import timezone
from django.utils.html import format_html




class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'
   
class RepairLogForm(forms.ModelForm):
    class Meta:
        model = RepairLog
        exclude = ['user_stamp', 'date_created']  
        fields = '__all__'
    
### INLINES############################################################################################################################################

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
   
### ADMIN    #########################################################
   
class WorkOrderAdmin(admin.ModelAdmin):
    form = WorkOrderForm
    inlines = [RepairLogInline]

    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox

    list_display = ('status', 'created_by', 'date_created','date_closed', 'display_image')
    raw_id_fields = ('machine',)
    readonly_fields = ('date_created', 'created_by', 'date_closed','display_image_preview',)
    
    def save_model(self, request, obj, form, change):
        if not obj.id:
            print("Hi")
            obj.user_stamp = request.user
            obj.date_created = timezone.now()
      
        obj.save()

    def display_image(self, obj):
        return obj.image_url()
    display_image.short_description = 'Image'

    def display_image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image_url())


    display_image.short_description = 'Image'



    
    


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
    
admin.site.register(WorkOrder,  WorkOrderAdmin)
admin.site.register(RepairLog, RepairLogAdmin)
