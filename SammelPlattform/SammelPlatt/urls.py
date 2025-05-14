# SammelPlatt/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.rezensionen_anzeigen, name='reviews'),
    path('rezension-erstellen/', views.rezension_erstellen, name='rezension_erstellen'),
]

