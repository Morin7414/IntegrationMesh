from django.urls import path
from . import views
app_name = 'slot_machines'

urlpatterns = [
       path('import-serials/', views.import_serials, name="import_serials"),
       path('sync-all-asset-trackers/', views.sync_all_asset_trackers, name='sync_all_asset_trackers'),
]