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

        # UID aus E-Mail extrahieren, z. B. "max.muster@schule.local" → "max.muster"
        uid = email.split('@')[0] if email else ''

        # === LDAP-Konfig ===
        from ldap3 import Server, Connection, SUBTREE
        LDAP_SERVER = 'ldaps://ldaps.htlwy.at'
        BIND_DN = 'cn=ldap-ro,ou=services,dc=schule,dc=local'
        BIND_PASSWORD = '8b6d0aa2-ee34-412e-a50b-9ba991c512bd'
        BASE_DN = 'ou=users,dc=schule,dc=local'

        try:
            # Verbindung zum LDAP-Server mit read-only Account
            server = Server(LDAP_SERVER, use_ssl=True)
            conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD, auto_bind=True)

            # Benutzer-DN suchen
            conn.search(BASE_DN, f'(uid={uid})', search_scope=SUBTREE, attributes=['cn', 'uid'])
            if not conn.entries:
                return JsonResponse({'error': 'Benutzer nicht gefunden'}, status=401)

            user_dn = conn.entries[0].entry_dn

            # Jetzt versuchen mit Benutzer-DN + Passwort zu binden
            user_conn = Connection(server, user=user_dn, password=password, auto_bind=True)

            if user_conn.bound:
                # Erfolg
                return JsonResponse({'message': 'Login erfolgreich'})
            else:
                return JsonResponse({'error': 'Login fehlgeschlagen'}, status=401)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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
    aktueller_ordner = get_object_or_404(Ordner, slug=slug)

    unterordner = Ordner.objects.filter(inordner=aktueller_ordner)
    fotos = aktueller_ordner.foto_set.all()

    return render(request, 'ordner_detail.html', {
        'aktueller_ordner': aktueller_ordner,
        'unterordner': unterordner,
        'fotos': fotos
    })


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
        parent_slug = data.get('parent')  # besser aus POST-Daten statt GET

        parent_ordner = Ordner.objects.filter(slug=parent_slug).first() if parent_slug else None

        # Prüfe auf Doppelung im gleichen Parent
        if Ordner.objects.filter(slug=slug, inordner=parent_ordner).exists():
            return JsonResponse({'success': False, 'error': 'Ordner mit diesem Namen existiert bereits im aktuellen Ordner'})

        # Pfad korrekt zusammensetzen
        pfad = f"{parent_ordner.pfad}{slug}/" if parent_ordner else "/"

        ordner = Ordner.objects.create(
            titel=titel,
            pfad=pfad,
            slug=slug,
            inordner=parent_ordner
        )

        return JsonResponse({'success': True, 'slug': ordner.slug})
    
    return JsonResponse({'success': False, 'error': 'Ungültige Methode'})

@csrf_exempt
def ordner_loeschen(request, slug):
    if request.method == 'DELETE':
        try:
            ordner = get_object_or_404(Ordner, slug=slug)
            ordner.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Ungültige Methode'}, status=405)

@csrf_exempt
def ordner_umbenennen(request, slug):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            neuer_name = data.get('name', '').strip()

            if not neuer_name:
                return JsonResponse({'success': False, 'error': 'Kein neuer Name angegeben'})

            ordner = get_object_or_404(Ordner, slug=slug)
            ordner.titel = neuer_name
            ordner.slug = slugify(neuer_name)
            ordner.save()

            return JsonResponse({'success': True, 'neuer_slug': ordner.slug})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Ungültige Methode'}, status=405)

from .models import Foto, Ordner, Kategorie
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import datetime


@csrf_exempt
def upload_foto(request):
    print("Upload-Foto View aufgerufen")
    if request.method == 'POST':
        print("POST Request empfangen")
        try:
            beschreibung = request.POST.get('beschreibung', 'süßes Hundefoto')
            slug = request.POST.get('slug')
            print(f"Beschreibung: {beschreibung}, Slug: {slug}")

            ordner = Ordner.objects.get(slug=slug)
            bild = request.FILES.get('bild')

            if not bild:
                print("Kein Bild im Request")
                return JsonResponse({'success': False, 'error': 'Kein Bild hochgeladen'})

            print(f"Bild empfangen: {bild.name}")

            neues_foto = Foto.objects.create(
                beschreibung=beschreibung,
                ordid=ordner,
                hochladedatum=datetime.date.today(),
                foto=bild,
                gesamtbewertung=0.0
            )

            print("Foto erfolgreich gespeichert")
            return JsonResponse({'success': True, 'foto_id': neues_foto.fotoid})
        except Exception as e:
            print(f"Fehler beim Upload: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        print("Kein POST Request")
    return HttpResponseBadRequest('Nur POST erlaubt')



import base64
from django.shortcuts import get_object_or_404, render
from .models import Foto, Ordner

def galerie_ordner_detail(request, slug):
    aktueller_ordner = get_object_or_404(Ordner, slug=slug)
    unterordner = Ordner.objects.filter(inOrdner=aktueller_ordner)
    fotos = Foto.objects.filter(ordid=aktueller_ordner)

    return render(request, 'ordner_detail.html', {
        'aktueller_ordner': aktueller_ordner,
        'unterordner': unterordner,
        'fotos': fotos,
    })


from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse

def foto_anzeigen(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id)
    return FileResponse(foto.foto.open(), content_type='image/jpeg')