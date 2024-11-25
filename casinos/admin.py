from django.contrib import admin
from .models import Casino

# Register your models here.
@admin.register(Casino)
class CasinoAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('casino_id', 'casino_name', )
    # Fields to enable search functionality
    search_fields = ('casino_id', 'casino_name', )
    # Fields to filter by in the admin interface
  #  list_filter = ('casino_location',)
    # Read-only fields
  #  readonly_fields = ('casino_id',)
    # Customize form fieldsets for better organization
    '''
    fieldsets = (
        (None, {
            'fields': ('casino_id', 'casino_name', 'casino_location', 'logo')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('logo',),
        }),
    )

    def logo_display(self, obj):
        """Display the casino logo in the admin panel."""
        if obj.logo:
            return f"<img src='{obj.logo.url}' alt='{obj.casino_name}' style='width: 50px; height: auto;'>"
        return "No Logo"
    logo_display.allow_tags = True  # Mark as safe for HTML rendering
    logo_display.short_description = "Logo"  # Admin column header

    
    '''