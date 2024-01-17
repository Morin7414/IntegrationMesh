from django.contrib import admin
from .models import  WorkOrder
from .models import  RepairLog
from django import forms
from django.utils import timezone
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.utils.html import mark_safe
from datetime import datetime


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'
   
class RepairLogForm(forms.ModelForm):
    class Meta:
        model = RepairLog
        #exclude = ['user_stamp', 'date_created']  
        fields = '__all__'
       # widgets = {
         # 'description': CKEditorWidget(),
       # }

### INLINES############################################################################################################################################

class RepairLogInline(admin.TabularInline):
    model = RepairLog
   
    list_display = ('timestamp', 'reason_for_repair', 'user_stamp','status',)
    readonly_fields = ('timestamp', 'reason_for_repair', 'get_diagnostics','user_stamp','status',)
    
    extra = 1
    ordering = ('-timestamp',) 
    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing records
    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting existing records
    def has_add_permission(self, request, obj=None):
        # Disable the "Add another" button
         return False
    def get_diagnostics(self, obj):
        return mark_safe(obj.diagnostics)
    get_diagnostics.short_description = 'diagnostics'

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # Exclude the 'diagnostics' field
        fields = [field for field in fields if field != 'diagnostics']
        return fields
    

        # Set the timestamp to the current time
   
### ADMIN    #########################################################
   
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ( 'status',)
    list_filter = ('status',)
    form = WorkOrderForm
    inlines = [RepairLogInline]
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    list_display = ('machine','status', 'created_by',  'reason_for_repair', 'date_created','date_closed',)
    raw_id_fields = ('machine',)
    readonly_fields = ('date_created', 'created_by', 'date_closed','display_image',)

    fieldsets = (
        ('Work Order Information', {
            'fields': ('status', 'machine', 'date_created', 'date_closed', 'created_by', 'image', 'display_image',),
        }),
         ('Troubleshooting & Repair', {
            'fields': ('reason_for_repair', 'diagnostics'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
       

        if not obj.created_by:
            obj.created_by = request.user

         # Check if the status is 'In Service'
        if obj.status == 'In Service' and not obj.date_closed:
            obj.date_closed = datetime.now()

        elif obj.status != 'In Service':
        # If status is not 'In Service', clear date_closed
            obj.date_closed = None

    
       
        super().save_model(request, obj, form, change)

        RepairLog.objects.create(repair_log=obj, status=obj.status, user_stamp=request.user, reason_for_repair=obj.reason_for_repair, diagnostics =obj.diagnostics)
        obj.diagnostics = "" 
        obj.save()

    
    
    
    def display_image(self, obj):
        return format_html('<img src="{}" style="max-height: 600px; max-width: 600px;" />'.format(obj.image.url))
    

 
     

class RepairLogAdmin(admin.ModelAdmin):
    form = RepairLogForm
    list_display = ('repair_log', 'diagnostics',  'timestamp','user_stamp')
   # actions_on_top = False  # Remove actions dropdown from the top
   # actions = None  # Disable the selection checkbox
    def has_module_permission(self, request):
        # This method determines whether the module (app) is shown in the admin index.
        # Returning False will hide it from the navigation bar.
        return False

 

  
    
admin.site.register(WorkOrder,  WorkOrderAdmin)
admin.site.register(RepairLog, RepairLogAdmin)
