from django.urls import path
from . import views
app_name = 'departmental_assets'

urlpatterns = [
       path('import-data/', views.import_operational_assets, name='import_operational_assets'),
]