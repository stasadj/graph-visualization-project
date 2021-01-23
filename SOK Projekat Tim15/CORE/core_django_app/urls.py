from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plagini/', views.prikazi_plagine, name="plagini"),

]
