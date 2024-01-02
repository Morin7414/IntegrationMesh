# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('import-file-1/', views.import_file_1, name='import_file_1'),
    path('import-file-2/', views.import_file_2, name='import_file_2'),
]