from django.contrib import admin
from .models import  WorkOrder
from .models import  RepairLog
from django import forms
from django.utils import timezone
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from ckeditor.widgets import CKEditorWidget
from django.db import models


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'
   
class RepairLogForm(forms.ModelForm):
    class Meta:
        model = RepairLog
        #exclude = ['user_stamp', 'date_created']  
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),
        }

### INLINES############################################################################################################################################

class RepairLogInline(admin.TabularInline):
    model = RepairLog
    formfield_overrides = {
       models.TextField: {'widget': CKEditorWidget},
    }
    
    form = RepairLogForm
   # formset = RelatedModelInlineFormSet  # Use the custom formset
    readonly_fields = ('timestamp', 'user_stamp', 'status', )
    extra = 1
    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing records
    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting existing records
   # def has_add_permission(self, request, obj=None):
        # Disable the "Add another" button
      #  return False
    
    def save_model(self, request, obj, form, change):
        # Set the userstamp to the current logged-in user
       
        if request.user.is_authenticated:
            obj.timestamp = timezone.now()
        obj.save()


        # Set the timestamp to the current time
   
### ADMIN    #########################################################
   
class WorkOrderAdmin(admin.ModelAdmin):
    
    form = WorkOrderForm
    inlines = [RepairLogInline]
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    list_display = ('status', 'created_by', 'date_created','date_closed', 'reason_for_repair')
    raw_id_fields = ('machine',)
    readonly_fields = ('date_created', 'created_by', 'date_closed','display_image')
    def save_model(self, request, obj, form, change):
        if not obj.id:
            print("Hi")
            obj.user_stamp = request.user
            obj.date_created = timezone.now()
        obj.save()
    def display_image(self, obj):
        return format_html('<img src="{}" style="max-height: 1000px; max-width: 1000px;" />'.format(obj.image.url))
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        RepairLog.objects.create(repair_log=obj, status=obj.status, user_stamp=obj.created_by)
     

class RepairLogAdmin(admin.ModelAdmin):
    form = RepairLogForm
    list_display = ('repair_log', 'diagnostics',  'timestamp','user_stamp')
   # actions_on_top = False  # Remove actions dropdown from the top
   # actions = None  # Disable the selection checkbox

    def save_model(self, request, obj, form, change):
        if not obj.id:
            print("Hi")
            obj.user_stamp = request.user
        obj.save()

  
    
admin.site.register(WorkOrder,  WorkOrderAdmin)
admin.site.register(RepairLog, RepairLogAdmin)
