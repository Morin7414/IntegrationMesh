from django.contrib import admin
from .models import  WorkOrder
from .models import  RepairLog
from django import forms
from django.utils import timezone
from django.utils.html import format_html
import boto3
import base64

def convert_image_to_base64(modeladmin, request, queryset):
    for obj in queryset:
        s3_url = obj.image.url  # Replace 'image_field' with your actual image field
        base64_image = get_base64_from_s3_url(s3_url)
        # Do something with the base64_image, for example, print it
        print(base64_image)
convert_image_to_base64.short_description = "Convert selected images to Base64"

def get_base64_from_s3_url(s3_url):
    # Assume your S3 bucket is public and the images are accessible without authentication
    # If your bucket is private, you need to configure Boto3 with your AWS credentials
    # and update the S3 client accordingly
    
    s3_client = boto3.client('s3')
    print (s3_client)
    response = s3_client.get_object(Bucket='fortfolio', Key=s3_url.split('/')[-1])
    image_content = response['Body'].read()
    base64_image = base64.b64encode(image_content).decode('utf-8')
    return base64_image


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
    actions = [convert_image_to_base64]
    form = WorkOrderForm
    inlines = [RepairLogInline]

    actions_on_top = False  # Remove actions dropdown from the top
    actions = None  # Disable the selection checkbox

    list_display = ('status', 'created_by', 'date_created','date_closed')
    raw_id_fields = ('machine',)
    readonly_fields = ('date_created', 'created_by', 'date_closed',)
    
    def save_model(self, request, obj, form, change):
        if not obj.id:
            print("Hi")
            obj.user_stamp = request.user
            obj.date_created = timezone.now()
      
        obj.save()

    def display_image(self, obj):
        return obj.image_url()
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
