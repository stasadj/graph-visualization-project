from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plagini/', views.prikazi_plagine, name="plagini"), #posle obrisati, sluzi za ispis instaliranih plagina, dobar test da li su dobro ucitani

]
