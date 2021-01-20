from django.shortcuts import render
from django.apps.registry import apps #dina dodala

# Create your views here.


def index(request):
    title = apps.get_app_config('core_django_app').verbose_name
    return render(request, 'index.html', {"title": title})

