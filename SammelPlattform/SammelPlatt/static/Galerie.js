function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});

/**
 * Ordner hinzufügen.
 * @param {string|null} parentSlug Optional: Slug des Parent-Ordners.
 */
function Ordnerhinzufuegen(parentSlug = null) {
    const alleEingaben = document.querySelectorAll('.ordner-name-input');
    for (const eingabe of alleEingaben) {
        if (eingabe.value.trim() === '') {
            alert('Bitte gib zuerst einen Namen für den bestehenden Ordner ein.');
            eingabe.focus();
            return;
        }
    }

    const ordnerName = prompt("Ordnername eingeben:");
    if (!ordnerName || ordnerName.trim() === '') {
        alert("Ordnername darf nicht leer sein.");
        return;
    }

    const payload = { name: ordnerName.trim() };
    if (parentSlug) {
        payload.parent = parentSlug;
    }

    fetch('/api/ordner-erstellen/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Ordner im DOM anzeigen
            const neuerOrdner = document.createElement('div');
            neuerOrdner.className = 'ordner';

            const nameInput = document.createElement('input');
            nameInput.type = 'text';
            nameInput.className = 'ordner-name-input';
            nameInput.value = ordnerName;
            nameInput.readOnly = true;

            neuerOrdner.appendChild(nameInput);

            const bild = document.createElement('img');
            bild.src = ORDNER_BILD_URL;
            bild.alt = 'Ordnerbild';
            bild.className = 'ordner-bild';
            bild.style.width = '200px';

            bild.addEventListener('click', () => {
                window.location.href = `/galerie/${data.slug}/`;
            });

            neuerOrdner.appendChild(bild);

            const ordnerContainer = document.getElementById('Ordner');
            ordnerContainer.appendChild(neuerOrdner);

            // Optional: Weiterleitung
            // window.location.href = `/galerie/${data.slug}/`;
        } else {
            alert(data.error || "Fehler beim Erstellen des Ordners.");
        }
    })
    .catch(error => {
        console.error("Fehler:", error);
        alert("Ein Fehler ist aufgetreten.");
    });
}

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : '';
}

function OrdnerUmbenennen(slug) {
    const neuerName = prompt("Neuer Ordnername:");

    if (!neuerName || neuerName.trim() === '') {
        alert("Der neue Ordnername darf nicht leer sein.");
        return;
    }

    fetch(`/api/ordner-umbenennen/${slug}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ name: neuerName.trim() })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Ordner erfolgreich umbenannt!");
            location.reload(); // oder den Namen im DOM direkt ändern
        } else {
            alert(data.error || "Fehler beim Umbenennen.");
        }
    })
    .catch(error => {
        console.error("Fehler beim Umbenennen:", error);
        alert("Ein Fehler ist aufgetreten.");
    });
}

function OrdnerLoeschen(slug) {
    if (!confirm("Möchtest du diesen Ordner wirklich löschen?")) {
        return;
    }

    fetch(`/api/ordner-loeschen/${slug}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Ordner gelöscht.");
            location.reload(); // oder entferne das Element per JS aus dem DOM
        } else {
            alert(data.error || "Fehler beim Löschen.");
        }
    })
    .catch(error => {
        console.error("Fehler beim Löschen:", error);
        alert("Ein Fehler ist aufgetreten.");
    });
}
