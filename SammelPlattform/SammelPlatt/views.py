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

from django.shortcuts import render
from .models import Bewertung

def reviews(request):
    bewertungen = Bewertung.objects.all()
    return render(request, 'Reviews.html', {'bewertungen': bewertungen})


def galerie(request):
    ordner = Ordner.objects.filter(inordner=None)
    return render(request, 'Galerie.html', {'ordner': ordner})


from django.shortcuts import render, get_object_or_404
from .models import Foto

def foto_detail(request, id):
    foto = get_object_or_404(Foto, fotoid=id)
    absolute_image_url = request.build_absolute_uri(foto.foto.url)
    absolute_page_url = request.build_absolute_uri()
    return render(request, 'foto_detail.html', {
        'foto': foto,
        'absolute_image_url': absolute_image_url,
        'absolute_page_url': absolute_page_url,
    })


from django.shortcuts import get_object_or_404, render
from .models import Ordner, Foto

def ordner_detail(request, slug):
    aktueller_ordner = get_object_or_404(Ordner, slug=slug)

    unterordner = Ordner.objects.filter(inordner=aktueller_ordner)
    fotos = Foto.objects.filter(ordid=aktueller_ordner)

    # Füge jedem Foto die absolute URL hinzu
    for foto in fotos:
        foto.full_url = request.build_absolute_uri(foto.foto.url)

    return render(request, 'ordner_detail.html', {
        'aktueller_ordner': aktueller_ordner,
        'unterordner': unterordner,
        'fotos': fotos,
    })
from django.shortcuts import get_object_or_404, redirect
from .models import Foto  # ggf. anpassen

def bild_loeschen(request, fotoid):
    bild = get_object_or_404(Foto, fotoid=fotoid)
   
    # Optional: Überprüfen, ob der Benutzer berechtigt ist
    if request.method == 'POST':
        ordner_slug = bild.ordid.slug  # für Redirect
        bild.foto.delete()  # löscht Datei vom Speicher
        bild.delete()       # löscht Datenbankeintrag
        return redirect('ordner_detail', slug=ordner_slug)
 
    return redirect('ordner_detail', slug=bild.ordner.slug)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Foto

import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from .models import Foto

def bild_bearbeiten(request, fotoid):
    bild = get_object_or_404(Foto, fotoid=fotoid)

    if request.method == 'POST':
        beschreibung = request.POST.get('beschreibung', '')
        neues_foto = request.FILES.get('foto')
        bearbeitetes_bild = request.POST.get('bearbeitetes_bild')

        bild.beschreibung = beschreibung

        if bearbeitetes_bild:
            try:
                format, imgstr = bearbeitetes_bild.split(';base64,')  # z.B. 'data:image/png;base64,...'
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f"bearbeitet_{bild.fotoid}.{ext}")
                bild.foto.delete(save=False)  # altes Bild löschen, aber nicht sofort speichern
                bild.foto = data
            except Exception as e:
                print(f"Fehler beim Verarbeiten des Base64-Bildes: {e}")

        elif neues_foto:
            bild.foto.delete(save=False)  # optional: altes Bild löschen
            bild.foto = neues_foto

        bild.save()
        return redirect('ordner_detail', slug=bild.ordid.slug)

    return render(request, 'bild_bearbeiten.html', {'bild': bild})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import Bewertung, Nutzer, Foto


def rezensionen_anzeigen(request):
    bewertungen = Bewertung.objects.all()
    return render(request, 'Reviews.html', {'bewertungen': bewertungen})


@csrf_exempt
def bewertung_erstellen(request):
    if request.method == 'POST':
        try:
            daten = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ungültiges JSON'}, status=400)

        titel = daten.get('titel')
        beschreibung = daten.get('text')
        sterne = daten.get('sterne')

        # Nutzer holen (oder anpassen mit User-Login)
        nutzer = Nutzer.objects.first()
        if not nutzer:
            return JsonResponse({'error': 'Kein Nutzer vorhanden'}, status=404)

        # Foto holen (optional, z.B. erstes Foto)
        foto = Foto.objects.first()
        if not foto:
            return JsonResponse({'error': 'Kein Foto vorhanden'}, status=404)

        bewertung = Bewertung(
            titel=titel,
            beschreibung=beschreibung,
            sternezahl=sterne,
            nutzerid=nutzer,
            fotoid=foto
        )
        bewertung.save()

        return JsonResponse({
            'titel': bewertung.titel,
            'beschreibung': bewertung.beschreibung,
            'sterne': bewertung.sternezahl,
        })

    return JsonResponse({'error': 'Nur POST erlaubt'}, status=400)
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

import qrcode
from io import BytesIO
from django.http import HttpResponse

def qr_code_view(request, fotoid):
    foto = get_object_or_404(Foto, fotoid=fotoid)
    img_url = request.build_absolute_uri(foto.foto.url)

    qr = qrcode.make(img_url)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response
import os

def delete_fotos_and_files(ordner):
    for foto in ordner.foto_set.all():
        if foto.foto:
            filepath = foto.foto.path
            os.path.isfile(filepath)
            os.remove(filepath)
        foto.delete()

def delete_ordner_recursively(ordner):
    # Alle Unterordner rekursiv löschen
    for sub_ordner in Ordner.objects.filter(inordner=ordner):
        delete_ordner_recursively(sub_ordner)
    # Fotos löschen (inkl. Dateien)
    delete_fotos_and_files(ordner)
    # Ordner löschen
    ordner.delete()

def ordner_loeschen(request, ordnerid):
    ordner = get_object_or_404(Ordner, pk=ordnerid)

    if request.method == 'POST':
        # Ordner inkl. Unterordner und Fotos löschen
        delete_ordner_recursively(ordner)
        return redirect('galerie')  # Oder wie der Name deiner Galerie-Startseite heißt

    return render(request, 'ordner_bestaetigung.html', {'ordner': ordner})

