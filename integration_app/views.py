# myapp/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'integration_app/index.html')

def import_file_1(request):
    # Handle import logic for file 1
    return render(request, 'integration_app/import_file_1.html')

def import_file_2(request):
    # Handle import logic for file 2
    return render(request, 'integration_app/import_file_2.html')