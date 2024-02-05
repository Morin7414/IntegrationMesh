
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views




urlpatterns = [
    
    #  path('photo/<int:photo_id>/', display_photo, name='display_photo'),
  #    path('image_data/<str:image_key>/', image_data, name='image_data'),
    path('get_machine_details/', views.get_machine_details, name='get_machine_details'),
]


