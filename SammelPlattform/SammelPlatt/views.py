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

def rezensionen_anzeigen(request):
    # Alle Bewertungen aus der Datenbank holen
    bewertungen = Bewertung.objects.all()  # Alle Bewertungen abfragen
    
    # Daten an das Template übergeben
    return render(request, 'Reviews.html', {'Rezension': bewertungen}) 

import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Bewertung

@csrf_exempt  # oder verwende den standard CSRF-Mechanismus mit csrftoken im Header
def rezension_erstellen(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Nur POST erlaubt")
    try:
        payload = json.loads(request.body)
        text = payload.get('text', '').strip()
        sterne = int(payload.get('sterne', 5))
        titel = payload.get('titel', '')[:25]  # max_length beachten

        # Einfügen in die DB
        bew = Bewertung.objects.create(
            titel=titel or '-',
            beschreibung=text,
            sternezahl=sterne,
            # ggf. referenzen zu Nutzer/Fotos hier setzen
        )

        return JsonResponse({
            'id': bew.bewertungid,
            'titel': bew.titel,
            'beschreibung': bew.beschreibung,
            'sternezahl': bew.sternezahl,
        }, status=201)
    except Exception as e:
        return HttpResponseBadRequest(f"Fehler: {e}")
   