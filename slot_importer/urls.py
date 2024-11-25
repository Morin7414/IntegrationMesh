from django.urls import path
from . import views
app_name = 'slot_importer'

urlpatterns = [
       path('upload-csv/', views.import_csv, name="slotmachine_upload_csv"),

]