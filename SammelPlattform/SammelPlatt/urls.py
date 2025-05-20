# SammelPlatt/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.rezensionen_anzeigen, name='reviews'),
    path('rezension-erstellen/', views.rezension_erstellen, name='rezension_erstellen'),
    path('galerie/', views.galerie, name='galerie'),
    path('galerie/<slug:slug>/', views.ordner_detail, name='ordner_detail'),
    path('api/ordner-erstellen/', views.ordner_erstellen, name='ordner_erstellen'),
]