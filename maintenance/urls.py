from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import SlotMachineMaintenanceFormViewSet,CurrentUserView,SlotMachineMaintenanceFormCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



'''
from .views import CasinoOutOfServiceView
urlpatterns = [
    path('casino-out-of-service/', CasinoOutOfServiceView.as_view(), name='casino-out-of-service'),
  
]

'''
router = DefaultRouter()
router.register(r'maintenanceforms', SlotMachineMaintenanceFormViewSet, basename='maintenanceforms')

urlpatterns = [
    path('api/', include(router.urls)),
   # path('api/token/', include('rest_framework_simplejwt.urls')),  # JWT endpoints
    path('api/openticket', SlotMachineMaintenanceFormCreateAPIView.as_view(), name='create-maintenance-form'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/me/', CurrentUserView.as_view(), name='current-user'),

    
]

print("Registered URL patterns:", urlpatterns)