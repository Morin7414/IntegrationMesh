from django.urls import path
from .views import MaintenanceStatusCountView,CasinoOutOfServiceCountView

urlpatterns = [
    path('maintenance-status-count/', MaintenanceStatusCountView.as_view(), name='maintenance-status-count'),
    path('casino-out-of-service-count/', CasinoOutOfServiceCountView.as_view(), name='casino-out-of-service-count'),
  
]
