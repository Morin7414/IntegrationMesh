from django.contrib import admin
from django import forms
from .models import Machine, RepairLog
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from django.forms import inlineformset_factory

# Register your models here.

class RepairLogAdminForm(forms.ModelForm):
    class Meta:
        model = RepairLog
        fields = '__all__'

class RepairLogInline(admin.TabularInline):
    model = RepairLog
    extra = 1
    form = RepairLogAdminForm
    fields = ['log_text', 'log_date', 'logged_by']
    readonly_fields = ['log_date', 'logged_by','logged_by']

    def has_delete_permission(self, request, obj=None):
        return False  # Disable the delete action
    
    def has_add_permission(self, request, obj=None):
        return False  # Disable the add action

    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly
        return list(set([field.name for field in self.model._meta.fields]))

class MachineAdminForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields readonly except for 'status'
        for field_name in self.fields:
            if field_name != 'status':
                self.fields[field_name].widget.attrs['readonly'] = True
                self.fields[field_name].widget.attrs['style'] = 'background-color: #f8f8f8;'

         # Customize the style for the 'status' field
        self.fields['status'].widget.attrs['style'] = 'background-color: yellow;'



class MachineAdmin(admin.ModelAdmin):
    list_display = ('assetNumber', 'serialNumber', 'gameTheme', 'modelID', 'status')
    search_fields = ['assetNumber', 'serialNumber', 'gameTheme', 'modelID', 'status']  # Add fields you want to search
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    
    inlines = [RepairLogInline]

    form = MachineAdminForm

    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly except for 'status'
        if obj:
            return [field.name for field in self.model._meta.fields if field.name != 'status']
        return []
    
    def has_delete_permission(self, request, obj=None):
        return False  # Disable the delete action
    def has_add_permission(self, request, obj=None):
        return False  # Disable the add action

  
    
class RepairLogAdmin(admin.ModelAdmin):
    actions_on_top = False  # Remove actions dropdown from the top
    search_fields = ['machine']  # Add fields you want to search
    list_display = ('machine', 'log_text', 'log_date', 'logged_by')
    actions = None  # Disable the selection checkbox




admin.site.register(Machine, MachineAdmin)
admin.site.register(RepairLog, RepairLogAdmin)

