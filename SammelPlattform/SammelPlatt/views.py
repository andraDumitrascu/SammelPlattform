from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, FileResponse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import Bewertung, Nutzer, Ordner, Foto, Kategorie

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

        uid = email.split('@')[0] if email else ''

        from ldap3 import Server, Connection, SUBTREE
        LDAP_SERVER = 'ldaps://ldaps.htlwy.at'
        BIND_DN = 'cn=ldap-ro,ou=services,dc=schule,dc=local'
        BIND_PASSWORD = '8b6d0aa2-ee34-412e-a50b-9ba991c512bd'
        BASE_DN = 'ou=users,dc=schule,dc=local'

        try:
            server = Server(LDAP_SERVER, use_ssl=True)
            conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD, auto_bind=True)
            conn.search(BASE_DN, f'(uid={uid})', search_scope=SUBTREE, attributes=['cn', 'uid'])
            if not conn.entries:
                return JsonResponse({'error': 'Benutzer nicht gefunden'}, status=401)

            user_dn = conn.entries[0].entry_dn

            user_conn = Connection(server, user=user_dn, password=password, auto_bind=True)

            if user_conn.bound:
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
    ordner = Ordner.objects.filter(inordner=None)
    return render(request, 'Galerie.html', {'ordner': ordner})

from django.shortcuts import get_object_or_404, render
from .models import Ordner, Foto

def ordner_detail(request, slug):
    aktueller_ordner = get_object_or_404(Ordner, slug=slug)

    unterordner = Ordner.objects.filter(inordner=aktueller_ordner)

    fotos = Foto.objects.filter(ordid=aktueller_ordner)

    return render(request, 'ordner_detail.html', {
        'aktueller_ordner': aktueller_ordner,
        'unterordner': unterordner,
        'fotos': fotos,
    })



def rezensionen_anzeigen(request):
    bewertungen = Bewertung.objects.all()
    return render(request, 'Reviews.html', {'bewertungen': bewertungen}) 

@csrf_exempt
def rezension_erstellen(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Nur POST erlaubt")

    try:
        payload = json.loads(request.body)
        text = payload.get('text', '').strip()
        sterne = int(payload.get('sterne', 5))
        titel = payload.get('titel', '')[:25]
        nutzer_id = payload.get('nutzerid')

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
            'nutzerid': nutzer.pk
        }, status=201)

    except Exception as e:
        return HttpResponseBadRequest(f"Fehler: {e}")

from django.conf import settings
import os
from django.core.files import File

@csrf_exempt
def ordner_erstellen(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            parent_id = data.get('parent')

            if not name:
                return JsonResponse({'success': False, 'error': 'Kein Name angegeben'}, status=400)

            parent_ordner = None

            base_slug = slugify(name)
            slug = base_slug
            counter = 1
            while Ordner.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            if parent_id:
                try:
                    parent_ordner = Ordner.objects.get(ordid=int(parent_id))
                    pfad = f"{parent_ordner.pfad}/{slug}"
                except Ordner.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Übergeordneter Ordner existiert nicht'}, status=400)
            else:
                pfad = slug  # root-Ordner

            neuer_ordner = Ordner(
                titel=name,
                pfad=pfad,
                slug=slug,
                inordner=parent_ordner
            )

            # Bild aus static laden und setzen
            ordner_bild_path = os.path.join(settings.BASE_DIR, 'static', 'Bilder', 'Ordner.png')
            with open(ordner_bild_path, 'rb') as f:
                neuer_ordner.bild.save('Ordner.png', File(f), save=False)

            neuer_ordner.save()

            return JsonResponse({
                'success': True,
                'titel': neuer_ordner.titel,
                'slug': neuer_ordner.slug,
                'OrdID': neuer_ordner.ordid,
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Ungültige JSON-Daten'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Nur POST erlaubt'}, status=405)


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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Ordner

@csrf_exempt
def ordner_loeschen(request, slug):
    if request.method == 'DELETE':
        try:
            ordner = get_object_or_404(Ordner, slug=slug)
            ordner.delete()
            return JsonResponse({'success': True, 'message': 'Ordner gelöscht'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Nur DELETE erlaubt'}, status=405)

@csrf_exempt
def upload_foto(request):
    if request.method == 'POST':
        try:
            beschreibung = request.POST.get('beschreibung', 'süßes Hundefoto')
            slug = request.POST.get('slug')

            ordner = Ordner.objects.get(slug=slug)
            bild = request.FILES.get('bild')

            if not bild:
                return JsonResponse({'success': False, 'error': 'Kein Bild hochgeladen'})

            neues_foto = Foto.objects.create(
                beschreibung=beschreibung,
                ordid=ordner,
                hochladedatum=datetime.date.today(),
                foto=bild,
                gesamtbewertung=0.0
            )

            return JsonResponse({'success': True, 'foto_id': neues_foto.fotoid})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return HttpResponseBadRequest('Nur POST erlaubt')

def galerie_ordner_detail(request, slug):
    aktueller_ordner = get_object_or_404(Ordner, slug=slug)
    unterordner = Ordner.objects.filter(inordner=aktueller_ordner)
    fotos = Foto.objects.filter(ordid=aktueller_ordner)

    return render(request, 'ordner_detail.html', {
        'aktueller_ordner': aktueller_ordner,
        'unterordner': unterordner,
        'fotos': fotos,
    })

def foto_anzeigen(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id)
    return FileResponse(foto.foto.open(), content_type='image/jpeg')
