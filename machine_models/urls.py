from django.urls import path
from . import views
app_name = 'machine_models'

urlpatterns = [
       path('import-machine-data/', views.import_machine_data, name='import_machine_data'),
]