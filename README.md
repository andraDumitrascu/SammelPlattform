# Social Solutions

## Überblick
Social Solutions ist eine Plattform zur effizienten Verwaltung von Fotos für schulische Social-Media-Kanäle. Lehrer, Klassensprecher und andere berechtigte Nutzer können Bilder hochladen, bearbeiten, speichern, organisieren und direkt auf Plattformen wie Instagram posten. Die Plattform sorgt für eine geordnete Ablage nach Klassen, Abteilungen oder Themen und bietet eine verschlüsselte Speicherung der Daten.

## Funktionen
- **Zentrale Sammlung** aller Schul-Social-Media-Fotos
- **Effizientes Hochladen, Bearbeiten und Verwalten** von Bildern
- **Einfache Veröffentlichung** auf Social-Media-Plattformen
- **Automatische Qualitätskontrolle** der Bilder
- **Strukturierte Ablage** nach Klassen, Abteilungen oder Themen
- **Verschlüsselte Speicherung** der Daten

## Technologie-Stack
- **Backend**: Django

- **Datenbank**: MySQL

- **Frontend**: HTML

- **Auth & Sicherheit**: Django Authentication

## Installation
Folge diesen Schritten, um das Projekt lokal einzurichten:

### 1. Repository klonen
```sh
git clone https://github.com/andraDumitrascu/SammelPlattform.git
cd SammelPlattform
```

### 2. Umgebung konfigurieren
Setze die Umgebungsvariablen in einer `.env`-Datei:
```
DJANGO_SECRET_KEY=dein_secret_key
DATABASE_URL=postgres://nutzer:passwort@localhost:5432/social_solutions
```

### 3. Abhängigkeiten installieren
```sh
pip install -r requirements.txt
```

### 4. Datenbank migrieren
```sh
python manage.py migrate
```

### 5. Server starten
```sh
python manage.py runserver
```

Anwendung im Browser öffnen: `http://localhost:8000`

## Mitwirken
Beiträge zum Projekt sind willkommen! Erstelle einen Fork, arbeite an Features und sende einen Pull Request.

## Lizenz
Dieses Projekt steht unter der Social Solutions Lizenz

## Nutzungsbedingungen
**Gültig ab: 25.03.2025**

Durch die Nutzung von Social Solutions stimmst du den folgenden Bedingungen zu:

### 1. Akzeptanz der Bedingungen
Mit der Nutzung dieser Plattform erklärst du dich mit diesen Nutzungsbedingungen und unserer Datenschutzrichtlinie einverstanden.

### 2. Beschreibung des Dienstes
Social Solutions ermöglicht es berechtigten Nutzern, Fotos für schulische Social-Media-Kanäle zu verwalten und zu veröffentlichen.

### 3. Verantwortlichkeiten der Nutzer
- Nutzer sind verantwortlich für alle Aktivitäten auf ihren Accounts.
- Es dürfen keine rechtswidrigen oder unangemessenen Inhalte hochgeladen werden.
- Die Plattform darf nicht für Spam oder unautorisierte Werbung genutzt werden.

### 4. Geistiges Eigentum
Alle Inhalte und Materialien von Social Solutions, einschließlich Code, Design und Datenbankstruktur, sind durch Urheberrechte geschützt.

### 5. Haftungsbeschränkung
Social Solutions übernimmt keine Haftung für Schäden oder Datenverluste, die durch die Nutzung der Plattform entstehen könnten.

### 6. Änderungen der Bedingungen
Wir behalten uns das Recht vor, diese Bedingungen jederzeit zu ändern. Änderungen treten mit Veröffentlichung auf dieser Seite in Kraft.

### 7. Anwendbares Recht
Diese Bedingungen unterliegen den Gesetzen von Österreich.

### 8. Kontakt
Bei Fragen zu den Nutzungsbedingungen kontaktiere uns unter: kitutorai@gmail.com


# Weiterführende Inhalte:
**Design mit Canva:** https://www.canva.com/design/DAGivXNQS8Q/uW9flFVHPAYnVDucnJlNIQ/
**Organisation mit Trello:** https://trello.com/b/VGpcwxyC/sammelplattform
**Präsentation mit Pitch:** https://app.pitch.com/app/presentation/1ac7fef8-a803-4f74-9a93-177a70472b15/12e9a8bb-5cb7-41c6-b141-685e03e8754c
