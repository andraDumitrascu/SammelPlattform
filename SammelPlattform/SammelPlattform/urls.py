"""
URL configuration for SammelPlattform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from SammelPlatt import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', views.home, name='home'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('login/', views.login_view, name='login'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('terms/', views.terms, name='terms'),
    path('reviews/', views.reviews, name='reviews'),
    path('galerie/', views.galerie, name='galerie'),
    path('', include('SammelPlatt.urls')),
    path('admin/', admin.site.urls),
    path('upload/', views.upload_foto, name='upload_foto'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
