# SammelPlatt/urls.py

from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('reviews/', views.rezensionen_anzeigen, name='reviews'),
    path('rezension-erstellen/', views.rezension_erstellen, name='rezension_erstellen'),
    path('galerie/', views.galerie, name='galerie'),
    path('galerie/<slug:slug>/', views.ordner_detail, name='ordner_detail'),
    path('api/ordner-erstellen/', views.ordner_erstellen, name='ordner_erstellen'),
    path('api/ordner-loeschen/<slug:slug>/', views.ordner_loeschen, name='ordner_loeschen'),
    path('api/ordner-umbenennen/<slug:slug>/', views.ordner_umbenennen, name='ordner_umbenennen'),
    path('login/', views.login_view, name='login'),
    path('upload/', views.upload_foto, name='upload_foto'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)