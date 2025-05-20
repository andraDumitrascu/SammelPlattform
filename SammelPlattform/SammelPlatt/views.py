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
    ordner = Ordner.objects.all()
    return render(request, 'Galerie.html', {'ordner': ordner})

def ordner_detail(request, slug):
    ordner = get_object_or_404(Ordner, slug=slug)
    return render(request, 'ordner_detail.html', {'ordner': ordner})

# views.py
def rezensionen_anzeigen(request):
    bewertungen = Bewertung.objects.all()
    return render(request, 'Reviews.html', {'bewertungen': bewertungen}) 


from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Bewertung
import json
from django.contrib.auth.models import User
from .models import Bewertung, Nutzer  # 👈 Importiere dein eigenes Modell

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
        nutzer_id = payload.get('nutzerid')  # 👈 ID vom Nutzer im JSON mitschicken
        print(f"Nutzer ID: {nutzer_id}"),
        if not text:
            return HttpResponseBadRequest("Text darf nicht leer sein")
        if not nutzer_id:
            return HttpResponseBadRequest("nutzer_id fehlt")

        nutzer = Nutzer.objects.get(pk=nutzer_id)  # 👈 hole den Nutzer aus der DB

        bew = Bewertung.objects.create(
            titel=titel or '-',
            beschreibung=text,
            sternezahl=sterne,
            nutzerid= nutzer  # 👈 nutzerid, nicht "User"
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

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Ordner
from django.utils.text import slugify

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
