from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plagini/', views.prikazi_plagine, name="plagini"), #posle obrisati, sluzi za ispis instaliranih plagina, dobar test da li su dobro ucitani
    path('odabir/plagina', views.odabir_plagina, name="odabir_plagina"),
    path('pokretanje/plagina', views.pokretanje_plagina, name="pokretanje_plagina"),

]
