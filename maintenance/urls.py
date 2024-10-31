from django.urls import path
from .views import CasinoOutOfServiceView
urlpatterns = [
    path('casino-out-of-service/', CasinoOutOfServiceView.as_view(), name='casino-out-of-service'),
  
]
