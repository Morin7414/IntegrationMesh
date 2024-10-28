from django.urls import path
from . import views
app_name = 'assets'

urlpatterns = [
       path('upload-csv/', views.import_csv, name="slotmachine_upload_csv"),
       path('import-serials/', views.import_serials, name="import_serials"),
       path('import-machine-data/', views.import_machine_data, name='import_machine_data'),
       path('sync-all-asset-trackers/', views.sync_all_asset_trackers, name='sync_all_asset_trackers'),


]