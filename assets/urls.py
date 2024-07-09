from django.urls import path
from . import views

urlpatterns = [
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('import_csv_view/', views.import_csv_view, name='import_csv_view'),
    path('show_updates/', views.show_updates, name='show_updates'),
    path('confirm_updates/', views.confirm_updates, name='confirm_updates'),
    path('success/', views.success, name='success'),
]