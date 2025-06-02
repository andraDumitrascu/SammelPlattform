function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let [key, value] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return '';
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});

function Rezesionhinzufuegen() {
    const eingabeContainer = document.createElement('div');
    eingabeContainer.className = 'Eingabe';

    const eingabeFeld = document.createElement('input');
    eingabeFeld.type = 'text';
    eingabeFeld.placeholder = 'Gib deine Rezension ein...';
    eingabeFeld.className = 'eingabe-feld';

    const hinzufuegenButton = document.createElement('button');
    hinzufuegenButton.textContent = 'Hinzufügen';
    hinzufuegenButton.className = 'hinzufuegen-button';

    hinzufuegenButton.onclick = async function () {
    const rezensionText = eingabeFeld.value.trim();
    if (rezensionText) {
        try {
            const response = await fetch("/bewertung-erstellen/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({
                    body: JSON.stringify({
    titel: rezensionText,
    text: rezensionText,
    sterne: 5
})

                })
            });

                if (!response.ok) {
                    if (response.status === 401) {
                        alert("Du musst eingeloggt sein, um eine Rezension zu schreiben.");
                        return;
                    }
                    throw new Error("Fehler beim Senden");
                }

                const data = await response.json();

                // Neue Rezensionselemente erstellen
                const neuerOrdner = document.createElement('div');
                neuerOrdner.className = 'review-box';

                const titel = document.createElement('h3');
                titel.textContent = data.titel;

               const sterne = document.createElement('p');
               sterne.style.display = 'none'; 

                const beschreibung = document.createElement('p');
                beschreibung.textContent = data.beschreibung;

                neuerOrdner.appendChild(titel);
                neuerOrdner.appendChild(sterne);
                neuerOrdner.appendChild(beschreibung);

                document.getElementById('rezension').appendChild(neuerOrdner);

                eingabeFeld.value = '';
                eingabeContainer.style.display = 'none';

            } catch (error) {
                alert("Fehler beim Speichern der Rezension");
                console.error(error);
            }
        } else {
            alert('Bitte gib eine Rezension ein.');
        }
    };

    eingabeContainer.appendChild(eingabeFeld);
    eingabeContainer.appendChild(hinzufuegenButton);
    document.getElementById('rezension').appendChild(eingabeContainer);
}
