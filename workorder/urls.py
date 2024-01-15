
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import display_photo



urlpatterns = [
   
      path('photo/<int:photo_id>/', display_photo, name='display_photo'),
 
]
