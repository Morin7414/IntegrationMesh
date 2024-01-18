from django.contrib import admin
from .models import  WorkOrder
from .models import  RepairLog
from django import forms
from django.utils.html import format_html
from django.utils.html import mark_safe, escape,strip_tags
from datetime import datetime
from django.template.defaultfilters import linebreaksbr



class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'
   
### INLINES############################################################################################################################################

class RepairLogInline(admin.TabularInline):
    model = RepairLog
    list_display = ('timestamp', 'reason_for_repair', 'user_stamp','status','display_thumbnail')
    readonly_fields = ('timestamp', 'reason_for_repair', 'get_diagnostics','user_stamp','status','display_thumbnail', )
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
        max_chars_before_wrap = 20
        text = strip_tags(obj.diagnostics)
        wrapped_text = f'<div style="word-wrap: break-word; max-width: {max_chars_before_wrap}ch;">{text}</div>'
        return mark_safe(wrapped_text)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # Exclude the 'diagnostics' field
        fields = [field for field in fields if field not in  ['diagnostics','image']]
        return fields
    
    def display_thumbnail(self, obj):
        if obj.image:
        # Assuming 'image' is the field storing the image file
            thumbnail_url = obj.image.url  # You need to adjust this based on your model structure
            s3_base_url = 'https://filefolio.s3.amazonaws.com/'  # Replace with your S3 bucket base URL

        # Check if thumbnail_url already contains the full S3 URL
            if thumbnail_url.startswith(s3_base_url):
                s3_url = thumbnail_url
            else:
                s3_url = s3_base_url + thumbnail_url

        # You can adjust the width and height as needed
            return format_html('<a href="{}" target="_blank"><img src="{}" style="max-width: 100px; max-height: 100px;" /></a>', s3_url, thumbnail_url)
        else:
            return ''

    
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
            'fields': ('status', 'machine', 'date_created', 'date_closed', 'created_by',),
        }),
         ('Troubleshooting & Repair', {
            'fields': ('image', 'reason_for_repair', 'diagnostics'),
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
        RepairLog.objects.create(repair_log=obj, status=obj.status, user_stamp=request.user, reason_for_repair=obj.reason_for_repair, diagnostics =obj.diagnostics, image = obj.image)
        obj.diagnostics = "" 
        obj.image = "" 
        obj.save()

    def display_image(self, obj):
        return format_html('<img src="{}" style="max-height: 600px; max-width: 600px;" />'.format(obj.image.url))
    

class RepairLogAdmin(admin.ModelAdmin):
    list_display = ('repair_log', 'diagnostics',  'timestamp','user_stamp')
   # actions_on_top = False  # Remove actions dropdown from the top
   # actions = None  # Disable the selection checkbox
    def has_module_permission(self, request):
        # This method determines whether the module (app) is shown in the admin index.
        # Returning False will hide it from the navigation bar.
        return False

 

  
    
admin.site.register(WorkOrder,  WorkOrderAdmin)
admin.site.register(RepairLog, RepairLogAdmin)
