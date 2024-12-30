from django.urls import path
from . import views
from .views import MachineListAPIView,SlotMachineDetailView

app_name = 'slot_importer'

urlpatterns = [
       path('upload-csv/', views.import_csv, name="slotmachine_upload_csv"),

       path('api/machines/', MachineListAPIView.as_view(), name='machine-list'),
       path('api/machines/<int:machine_serial_number>/', SlotMachineDetailView.as_view(), name='machine-detail'),

]