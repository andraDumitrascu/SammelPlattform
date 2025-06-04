

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

        // Sterne bei vorhandenen Rezensionen rendern
        document.querySelectorAll('.review-box').forEach(box => {
            const sterneWert = parseInt(box.dataset.sterne); // data-sterne Attribut auslesen
            const sterneDiv = box.querySelector('.sterne');
            if (sterneDiv && sterneWert) {
                renderSterne(sterneDiv, sterneWert);
            }
        });
    });

    function renderSterne(container, sterneWert) {
        container.innerHTML = '⭐'.repeat(sterneWert);
    }

    function Rezesionhinzufuegen() {
        const eingabeContainer = document.createElement('div');
        eingabeContainer.className = 'Eingabe flex flex-col space-y-2 mb-4';

        // Textfeld für Rezension
        const eingabeFeld = document.createElement('input');
        eingabeFeld.type = 'text';
        eingabeFeld.placeholder = 'Gib deine Rezension ein...';
        eingabeFeld.className = 'eingabe-feld px-2 py-1 border rounded';

        // Dropdown für Sternebewertung (mit ⭐-Emojis)
        const sterneAuswahl = document.createElement('select');
        sterneAuswahl.className = 'sterne-auswahl px-2 py-1 border rounded w-32 text-black';
        for (let i = 1; i <= 5; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = '⭐'.repeat(i);
            sterneAuswahl.appendChild(option);
        }

        // Button zum Hinzufügen
        const hinzufuegenButton = document.createElement('button');
        hinzufuegenButton.textContent = 'Hinzufügen';
        hinzufuegenButton.className = 'hinzufuegen-button bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded';

        // Elemente einfügen
        eingabeContainer.appendChild(eingabeFeld);
        eingabeContainer.appendChild(sterneAuswahl);
        eingabeContainer.appendChild(hinzufuegenButton);

        const rezensionContainer = document.getElementById('rezension');
        rezensionContainer.prepend(eingabeContainer);

        hinzufuegenButton.onclick = async function () {
            const rezensionText = eingabeFeld.value.trim();
            const sterneWert = parseInt(sterneAuswahl.value);

            if (rezensionText && sterneWert >= 1 && sterneWert <= 5) {
                try {
                    const response = await fetch("/bewertung-erstellen/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCSRFToken()
                        },
                        body: JSON.stringify({
                            titel: "Bewertung:",
                            text: rezensionText,
                            sterne: sterneWert
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

                    const neuerOrdner = document.createElement('div');
                    neuerOrdner.className = 'review-box p-4 border rounded shadow bg-white dark:bg-gray-800 dark:text-white';

                    // data-sterne Attribut hinzufügen, damit renderSterne darauf zugreifen kann
                    neuerOrdner.dataset.sterne = sterneWert;

                    const sterne = document.createElement('div');
                    sterne.className = 'sterne'; // Klasse für Sterncontainer
                    renderSterne(sterne, sterneWert); // Sterne mit Funktion rendern

                    const beschreibung = document.createElement('p');
                    beschreibung.textContent = rezensionText;

                    neuerOrdner.appendChild(sterne);
                    neuerOrdner.appendChild(beschreibung);

                    rezensionContainer.insertBefore(neuerOrdner, eingabeContainer.nextSibling);

                    eingabeFeld.value = '';
                    eingabeContainer.remove();

                } catch (error) {
                    alert("Fehler beim Speichern der Rezension");
                    console.error(error);
                }
            } else {
                alert('Bitte gib eine gültige Rezension mit Sternenanzahl ein.');
            }
        };
    }