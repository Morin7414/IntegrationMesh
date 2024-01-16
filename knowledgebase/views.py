from django.shortcuts import render
from .models import KnowledgeBase
# Create your views here.
def article_list(request):
    articles = KnowledgeBase.objects.all()
    return render(request, 'knowledgebase/knowledgebase.html', {'articles': articles})