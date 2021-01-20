
from django.urls import path
from . import views

#dina napravila fajl, valjda je okej
urlpatterns = [
    path('', views.index, name='index'), #ovde cemo dodavati jos
    ]