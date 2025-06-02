function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});

function createOrdnerElement(titel, ordnerId) {
    const ORDNER_BILD_URL = '/static/images/ordner.png';
    const neuerOrdner = document.createElement('div');
    neuerOrdner.className = 'ordner';

    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.className = 'ordner-name-input';
    nameInput.placeholder = 'Ordnername eingeben';
    nameInput.maxLength = 30;
    nameInput.autocomplete = 'off';
    nameInput.required = true;
    nameInput.value = titel;

    neuerOrdner.appendChild(nameInput);

    const bild = document.createElement('img');
    bild.src = ORDNER_BILD_URL;
    bild.alt = 'Ordnerbild';
    bild.className = 'ordner-bild';
    bild.style.width = '200px';

    neuerOrdner.appendChild(bild);

    bild.addEventListener('click', () => {
        const ordnerName = nameInput.value.trim();
        if (ordnerName) {
            window.location.href = `ordner.html?name=${encodeURIComponent(ordnerName)}`;
        } else {
            alert('Bitte zuerst einen Ordnernamen eingeben.');
        }
    });

    const loeschButton = document.createElement('button');
    loeschButton.textContent = 'Löschen';
    loeschButton.className = 'loesch-button';

    loeschButton.addEventListener('click', () => {
        if (confirm(`Ordner "${titel}" wirklich löschen?`)) {
            fetch(`/api/ordner-loeschen/${ordnerId}/`, { method: 'DELETE' })
            .then(res => res.json())
            .then(resp => {
                if (resp.success) {
                    neuerOrdner.remove();
                    alert('Ordner gelöscht');
                } else {
                    alert('Fehler beim Löschen: ' + resp.error);
                }
            })
            .catch(() => alert('Fehler beim Löschen'));
        }
    });

    neuerOrdner.appendChild(loeschButton);

    return neuerOrdner;
}

function Ordnerhinzufuegen() {
    // 1. Prüfen...
    const alleEingaben = document.querySelectorAll('.ordner-name-input');
    for (const eingabe of alleEingaben) {
        if (eingabe.value.trim() === '') {
            alert('Bitte gib zuerst einen Namen für den bestehenden Ordner ein.');
            eingabe.focus();
            return;
        }
    }

    // 2. Namen für neuen Ordner abfragen
    const ordnerName = prompt('Name für neuen Ordner eingeben:');
    if (!ordnerName || ordnerName.trim() === '') {
        alert('Bitte gib einen gültigen Ordnernamen ein.');
        return;
    }

    // 3. Fetch-Request
    fetch('/api/ordner-erstellen/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: ordnerName.trim(), parent: null })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Ordner "${data.titel}" wurde erstellt.`);

                const ordnerContainer = document.getElementById('Ordner');

                const neuerOrdner = createOrdnerElement(data.titel, data.OrdID);

                ordnerContainer.appendChild(neuerOrdner);

            } else {
                alert('Fehler: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Fehler:', error);
            alert('Fehler beim Erstellen des Ordners.');
        });
}




   

