from django.shortcuts import render

def home(request):
    return render(request, 'Home.html')

def kontakt(request):
    return render(request, 'Kontakt.html')

def login_view(request):
    return render(request, 'Log-In.html')

def datenschutz(request):
    return render(request, 'Datenschutz.html')

def terms(request):
    return render(request, 'terms.html')

def reviews(request):
    return render(request, 'Reviews.html')

def galerie(request):
    return render(request, 'Galerie.html')
    