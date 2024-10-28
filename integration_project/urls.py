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
#admin.site.index_template = 'admin/my_index.html'

urlpatterns = [
  #  path('admin/', custom_admin_site.urls), 
    path('admin/', admin.site.urls),

#   path('baton/', include('baton.urls')),

    path('assets/', include('assets.urls')),
    path('', lambda request: redirect('admin/')),  # Redirect to your app's URL
]
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


