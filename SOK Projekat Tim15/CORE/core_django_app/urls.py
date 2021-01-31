from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load/data', views.load_data, name="load_data"),
    path('visualize/data', views.visualize_data, name="visualize_data"),
    path('search/data', views.search_data, name="search_data"),
    path('filter/data', views.filter_data, name="filter_data")

]
