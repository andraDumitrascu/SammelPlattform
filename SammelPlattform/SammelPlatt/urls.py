# SammelPlatt/urls.py

from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('reviews/', views.rezensionen_anzeigen, name='reviews'),
    path('api/rezensionen/create/', views.rezension_erstellen, name='rezension_erstellen'),
    
]
