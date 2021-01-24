from django.shortcuts import render
from django.apps.registry import apps #dina dodala

# Create your views here.


def index(request):
    config = apps.get_app_config('core_django_app')
    title = config.verbose_name

    return render(request, 'index.html', {"title": title})


# Ovo posle obrisati
# Dobar test korektne instalacije i ucitavanja plagina unutar CORE
def prikazi_plagine(request):
    config = apps.get_app_config('core_django_app')
    plagini = config.load_data_plugins
    return render(request, "proba.html", {"title":"Index", "plugini_ucitavanje":plagini})


