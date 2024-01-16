from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField

class KnowledgeBase(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title