from django.contrib import admin
from workorder.models import WorkOrder






class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        print ('hi')

        # Your logic for fetching ticket counts
        open_tickets_count = WorkOrder.objects.filter(status='EGM DOWN - Awaiting Parts').count()
        closed_tickets_count = WorkOrder.objects.filter(status='Troubleshooting').count()

        # Add ticket counts to the context
        extra_context['open_tickets'] = open_tickets_count
        extra_context['closed_tickets'] = closed_tickets_count

        return super().index(request, extra_context=extra_context)

# Register your custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

custom_admin_site.site_header = "Custom Admin Dashboard"
custom_admin_site.site_title = "Custom Admin Dashboard"
custom_admin_site.index_title = "Welcome to the Custom Admin Dashboard"

# Register models with the custom admin site
#custom_admin_site.register(WorkOrder)