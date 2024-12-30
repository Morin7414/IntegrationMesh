"""
URL configuration for integration_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from baton.autodiscover import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
#from custom_admin.admin import custom_admin_site



admin.site.site_header = "Custom Admin Dashboard"
admin.site.site_title = "Custom Admin Dashboard"
admin.site.index_title = "Welcome to the Custom Admin Dashboard"


urlpatterns = [
    path('admin/', admin.site.urls),

    path('departmental_assets/', include('departmental_assets.urls')),
    path('machine_models/', include('machine_models.urls')),
   # path('slot_machines/', include('slot_machines.urls')),
    #path('slot_importer/', include('slot_importer.urls')),
    path('', include('slot_importer.urls')),

    path('', include('maintenance.urls')),  # This includes the urls from `myapp`
    path('', lambda request: redirect('admin/')),  # Redirect to your app's URL

]



