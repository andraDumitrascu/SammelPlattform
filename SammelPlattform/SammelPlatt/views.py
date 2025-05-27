from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Bewertung, Nutzer, Ordner
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    return render(request, 'Home.html')

def kontakt(request):
    return render(request, 'Kontakt.html')
@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        return render(request, 'Log-In.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ungültige JSON-Daten'}, status=400)

        user = authenticate(request, email=email, password=password)  # <- HIER wird dein Backend benutzt

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login erfolgreich'})
        else:
            return JsonResponse({'error': 'Ungültige Anmeldedaten'}, status=401)

def datenschutz(request):
    return render(request, 'Datenschutz.html')

def terms(request):
    return render(request, 'terms.html')

def reviews(request):
    return render(request, 'Reviews.html')

def galerie(request):
    ordner = Ordner.objects.all()
    return render(request, 'Galerie.html', {'ordner': ordner})

def ordner_detail(request, slug):
    ordner = get_object_or_404(Ordner, slug=slug)
    return render(request, 'ordner_detail.html', {'ordner': ordner})

def rezensionen_anzeigen(request):
    bewertungen = Bewertung.objects.all()
    return render(request, 'Reviews.html', {'bewertungen': bewertungen}) 

@csrf_exempt
def rezension_erstellen(request):
    print("POST-Request erhalten")
    if request.method != 'POST':
        return HttpResponseBadRequest("Nur POST erlaubt")

    try:
        print("Request body:", request.body)
        payload = json.loads(request.body)
        print("Payload:", payload)

        text = payload.get('text', '').strip()
        sterne = int(payload.get('sterne', 5))
        titel = payload.get('titel', '')[:25]
        nutzer_id = payload.get('nutzerid')
        print(f"Nutzer ID: {nutzer_id}")
        
        if not text:
            return HttpResponseBadRequest("Text darf nicht leer sein")
        if not nutzer_id:
            return HttpResponseBadRequest("nutzer_id fehlt")

        nutzer = Nutzer.objects.get(pk=nutzer_id)

        bew = Bewertung.objects.create(
            titel=titel or '-',
            beschreibung=text,
            sternezahl=sterne,
            nutzerid=nutzer
        )

        return JsonResponse({
            'id': bew.pk,
            'titel': bew.titel,
            'beschreibung': bew.beschreibung,
            'sternezahl': bew.sternezahl,
            'nutzerid': 1
        }, status=201)

    except Exception as e:
        print("Fehler beim Parsen/Speichern:", e)
        return HttpResponseBadRequest(f"Fehler: {e}")

@csrf_exempt
def ordner_erstellen(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        titel = data.get('name')
        if not titel:
            return JsonResponse({'success': False, 'error': 'Kein Name angegeben'})

        slug = slugify(titel)
        if Ordner.objects.filter(slug=slug).exists():
            return JsonResponse({'success': False, 'error': 'Ordner existiert bereits'})

        ordner = Ordner.objects.create(titel=titel, pfad='/', slug=slug)
        return JsonResponse({'success': True, 'slug': ordner.slug})
    
    return JsonResponse({'success': False, 'error': 'Ungültige Methode'})
