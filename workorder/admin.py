from django.conf import settings
from django.contrib import admin
from .models import  WorkOrder,RepairLog,PartsRequired
from assets.models import EGM
from django import forms
from django.utils.html import mark_safe, escape,strip_tags
from datetime import datetime
import logging
from django.forms import BaseInlineFormSet
from django.forms import ValidationError
#from custom_admin.admin import custom_admin_site
import boto3
from botocore.exceptions import ClientError
from django.urls import reverse
#logging.basicConfig(filename='debug.log', level=logging.DEBUG)

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'

class RepairLogInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if not form.cleaned_data.get('image'):
                    raise ValidationError('Image is required for each repair log entry.')

### INLINES ############################################################################################################################################

class PartsRequiredInline(admin.TabularInline):
    model = PartsRequired
    list_display = ('inventory', 'quantity','work_order','price_extension')
    readonly_fields = ('price_extension',)
    extra = 1
    raw_id_fields = ('inventory',)

 
class RepairLogInline(admin.TabularInline):
    model = RepairLog
   # formset = RepairLogInlineFormSet  # Use the custom formset
    list_display = ('timestamp', 'reason_for_repair', 'user_stamp','status','image_preview')
    readonly_fields = ('timestamp', 'reason_for_repair', 'get_diagnostics','user_stamp','status','image_preview', )
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
        max_chars_before_wrap = 120
        text = strip_tags(obj.diagnostics)
        wrapped_text = f'<div style="word-wrap: break-word; max-width: {max_chars_before_wrap}ch;">{text}</div>'
        return mark_safe(wrapped_text)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # Exclude the 'diagnostics' field
        fields = [field for field in fields if field not in  ['diagnostics','image']]
        return fields
    
    def image_preview(self, obj):
        try:
            if obj.image:
                logging.debug("Image_key!!!: %s", obj.image)
                image_key = obj.image
                s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name='ca-central-1', config=boto3.session.Config(signature_version='s3v4')) 
                url = s3_client.generate_presigned_url('get_object',
                                                  Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': f'{obj.image}'},
                                                  ExpiresIn=900) 
                                                 # ExpiresIn=900)  # URL expires in 1 hour
              #$  url = reverse('image_data', kwargs={'image_key': image_key})
             #   url = reverse('workorder:image_data') + f'?image_key={image_key}'
              # url = reverse('image_data', kwargs={'image_key': f'{image_key}'}
              #  return mark_safe(f'<a href="{url}" target="_blank"><img src="{url}" style="max-width: 100px; max-height: 100px;" /></a>')
                return mark_safe(f'<a href="{url}"><img src="{url}" style="max-width: 200px; max-height: 200px;" /></a>')
             
            else:
                return ""  # Return an empty string or any default value when there is no image
   
        except ClientError as e:
           
            return f"Error generating URL: {e}"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'
    
### ADMIN    #########################################################
# ('TROUBLESHOOTING', 'TROUBLESHOOTING'),
   #     ('AWAITNG PARTS', 'AWAITNG PARTS'),
    #    ('NEEDS MEM CLEAR', 'NEEDS MEM CLEAR'),
    #    ('MONITORING', 'MONITORING'),
    #    ('REPAIRED', 'REPAIRED'),



class StatusFilter(admin.SimpleListFilter):
    title = 'maintenance_ticket'
    parameter_name = 'maintenance_ticket'

    def lookups(self, request, model_admin):
        return (
            ('AWAITNG PARTS', 'AWAITNG PARTS'),
            ('NEEDS MEM CLEAR', 'NEEDS MEM CLEAR'),
            ('REPAIRED', 'REPAIRED'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'AWAITNG PARTS':
            return queryset.filter(status='AWAITNG PARTS')
        if self.value() == 'NEEDS MEM CLEAR':
            return queryset.filter(status='NEEDS MEM CLEAR')
        if self.value() == 'REPAIRED':
            return queryset.filter(status='REPAIRED')
        return queryset  
    
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ( 'maintenance_ticket',)
    list_filter = ('maintenance_ticket',)
 #   list_filter = (StatusFilter,)
    form = WorkOrderForm
    inlines = [PartsRequiredInline,RepairLogInline]
  #  actions_on_top = False  # Remove actions dropdown from the top
  #  actions = None  # Disable the selection checkbox

    list_display = ('asset_number','location', 'model','service_status', 'maintenance_ticket','created_by',  'current_subject','central_office_remarks', 'date_created','date_closed',)
    raw_id_fields = ('slot_machine',)

    readonly_fields = ('date_created', 'created_by', 'date_closed')
    readonly_fields = ( 'created_by',)

    fieldsets = (

        ('Machine Info', {
            'fields': ('service_status','slot_machine','asset_number','location','model',),
            'description': 'This section contains details related about the machine.'
        }),
        ('Troubleshooting & Repair', {
            'fields': ('image','current_subject','diagnostics'),
            
            'description': 'This section contains details related to troubleshooting and repair.'
        }),

        ('Work Order Information', {
            'fields': ('maintenance_ticket', 'date_created', 'date_closed', 'created_by', ),
            'classes': ('baton-tabs-init', 'baton-tab-group-fs-diagnostics--inline-repairlog','baton-tab-group-fs-COreference', ),
            'description': 'This section contains information about the work order.'
        }),
       #  ('Troubleshooting & Repair', {
        #    'fields': ('image','diagnostics'),
        #    'classes': ('tab-fs-diagnostics',),
        #    'description': 'This section contains details related to troubleshooting and repair.'
       # }),
         ('Central Office Reference', {
            'fields': ('central_office_remarks',),
            'classes': ('tab-fs-COreference',),
            'description': 'This section contains details related to troubleshooting and repair.'
        }),
      
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
       
        #if obj.status == 'REPAIR COMPLETED' and not obj.date_closed:
         #  obj.date_closed = datetime.now()
        elif obj.status != 'REPAIRED':
            obj.date_closed = None

        super().save_model(request, obj, form, change)
        RepairLog.objects.create(repair_log=obj, status=obj.service_status, user_stamp=request.user, reason_for_repair=obj.current_subject, diagnostics =obj.diagnostics, image = obj.image)
        obj.diagnostics = "" 
        obj.image = "" 
        obj.save()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_delete'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
      
    class Media:
        js = ('workorder/workorder_admin.js',)  # Path to your JavaScript file


class RepairLogAdmin(admin.ModelAdmin):
    list_display = ('repair_log', 'diagnostics',  'timestamp','user_stamp')
   # actions_on_top = False  # Remove actions dropdown from the top
   # actions = None  # Disable the selection checkbox
 
    def has_module_permission(self, request):
        # This method determines whether the module (app) is shown in the admin index.
        # Returning False will hide it from the navigation bar.
        return False

class PartRequiredAdmin(admin.ModelAdmin):
    list_display = 'inventory','quantity', 'remarks'
    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox
    raw_id_fields = ('inventory',)

# Register your custom admin site
#custom_admin_site = CustomAdminSite(name='custom_admin')
# Register models with the custom admin site
#custom_admin_site.register(WorkOrder, WorkOrderAdmin)
#custom_admin_site.register(RepairLog, RepairLogAdmin)
#custom_admin_site.register(PartsRequired, PartRequiredAdmin)
    

admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(RepairLog, RepairLogAdmin)
#admin.site.register(PartsRequired, PartRequiredAdmin)