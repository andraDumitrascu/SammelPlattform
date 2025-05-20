function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});

function Ordnerhinzufuegen() {
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

    // 1. AJAX-Request an Django
    fetch('/api/ordner-erstellen/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ name: ordnerName.trim() })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Optional: Sofort im DOM anzeigen (falls du nicht weiterleitest)
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

            // Alternativ: Direkt weiterleiten
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
