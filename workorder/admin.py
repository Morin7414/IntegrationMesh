from django.contrib import admin
from .models import  WorkOrder
from .models import PartRequired, RepairLog
from django import forms
from django.forms import BaseInlineFormSet
from django.utils import timezone


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        exclude = ['user_stamp', 'date_created']  # Exclude the user_stamp field from the form

# Register your models here.
class PartRequiredInline(admin.TabularInline):
    model = PartRequired
    extra = 1
    raw_id_fields = ('inventory',)

class RepairLogInline(admin.TabularInline):
    model = RepairLog
    extra = 1
    
    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing records

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting existing records
   

class WorkOrderAdmin(admin.ModelAdmin):
  #  exclude = ('user_stamp',)  # Exclude the user_stamp field from the form
    form = WorkOrderForm
    inlines = [RepairLogInline,PartRequiredInline]
    list_display = ('status', 'machine', 'user_stamp', 'date_created')
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    raw_id_fields = ('machine',)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user_stamp = request.user
            obj.timestamp = timezone.now()
        obj.save()

class RepairLogAdmin(admin.ModelAdmin):
    list_display = ('repair_log', 'troubleshooting_and_repair',  'timestamp','user_stamp')
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox

class PartRequiredAdmin(admin.ModelAdmin):
    list_display = 'inventory','quantity', 'comments'
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    raw_id_fields = ('inventory',)
    
    

admin.site.register(WorkOrder,  WorkOrderAdmin)
admin.site.register(RepairLog, RepairLogAdmin)
admin.site.register(PartRequired, PartRequiredAdmin)