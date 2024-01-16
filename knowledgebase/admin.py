from django.contrib import admin

# Register your models here.
from .models import KnowledgeBase

class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
  
    ordering = ('-created_at',)

admin.site.register(KnowledgeBase, KnowledgeBaseAdmin)