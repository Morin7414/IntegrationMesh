from django.contrib import admin, messages
from .models import EGM, SlotMachine, Model
from workorder.models import  WorkOrder

from django.utils.html import mark_safe
import logging
import boto3
from django.conf import settings

from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages

from import_export.admin import ImportExportModelAdmin
from .views import upload_csv, show_updates, confirm_updates, success, import_csv_view
#from custom_admin.admin import custom_admin_site

class WorkOrderInline(admin.TabularInline):
    model = WorkOrder
    fields  = ('maintenance_ticket','current_subject','date_created', 'date_closed', 'created_by',)
    readonly_fields =  ('maintenance_ticket','current_subject','date_created', 'date_closed','created_by',)
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing records
   
    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting existing records
   
    def has_add_permission(self, request, obj=None):
        # Disable the "Add another" button
         return False

class EGMAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    
 #   list_display = ('asset_number','bank','game_theme','serial_number','model_name')
    list_display = ('asset_number', 'location', 'model')
    search_fields = ['asset_number', 'location', 'model']  # Add fields you want to search
 #   inlines = [WorkOrderInline]
    
 #   actions_on_top = False  # Remove actions dropdown from the top
  #  actions = None  # Disable the selection checkbox
   # raw_id_fields = ('model_name',) #add this for many to many

class SlotMachineAdmin(admin.ModelAdmin):

    list_display = ('machine_serial_number', 'slot_machine_name','machine_model_name', 'status', 'last_updated')
    change_list_template = "admin/slot_machine_changelist.html"
    search_fields = ['machine_serial_number', 'slot_machine_name', 'status', 'last_updated']
    change_form_template = "admin/slot_machine_change_form.html"  # Use custom change form template
    actions = None  # Disable the selection checkbox

    def has_add_permission(self, request):
        # Disable the add button
        return False

    def has_delete_permission(self, request, obj=None):
        # Optionally, disable the delete button if needed
        return False

    def get_readonly_fields(self, request, obj=None):
        # Ensure all fields are read-only
        return [field.name for field in self.model._meta.fields]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload_csv/', self.admin_site.admin_view(upload_csv), name='upload_csv'),
            path('show_updates/', self.admin_site.admin_view(show_updates), name='show_updates'),
            path('confirm_updates/', self.admin_site.admin_view(confirm_updates), name='confirm_updates'),
            path('success/', self.admin_site.admin_view(success), name='success'),
        ]
        return custom_urls + urls

class ModelAdmin(admin.ModelAdmin):
    change_list_template = "admin/model_changelist.html"
    list_display = ('model_name', 'image_preview','manufacturer', 'model_type', 'machine_move_risk', 'current_amps')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import_csv_view/', self.admin_site.admin_view(import_csv_view), name='import_csv_view'),
            path('success/', self.admin_site.admin_view(success), name='success'),
        ]
        return custom_urls + urls
    
    def image_preview(self, obj):
        try:
            if obj.model_image:
                logging.debug("Image_key!!!: %s", obj.model_image)
                image_key = obj.model_image.name
                s3_client = boto3.client(
                    's3', 
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, 
                    region_name='ca-central-1', 
                    config=boto3.session.Config(signature_version='s3v4')
                )
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': image_key},
                    ExpiresIn=900
                )
                return mark_safe(f'<a href="{url}"><img src="{url}" style="max-width: 200px; max-height: 200px;" /></a>')
            else:
                return ""
        except Exception as e:
            logging.error(f"Error generating image preview: {e}")
            return ""

    image_preview.short_description = 'Image Preview'




admin.site.register(EGM, EGMAdmin)

admin.site.register(SlotMachine, SlotMachineAdmin)

admin.site.register(Model, ModelAdmin)






