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
    hinzufuegenButton.onclick = async function() {
        const rezensionText = eingabeFeld.value;
        if (rezensionText) {
            // ➤ Neue Rezension an Django senden
            try {
                const response = await fetch("/rezension-erstellen/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        titel: "Neue Rezension",
                        text: rezensionText,
                        sterne: 5
                        //nutzerid: nutzerid //Fehler!
                    })
                });

                if (!response.ok) throw new Error("Fehler beim Senden");

                const data = await response.json();

                // ➤ Ausgabe im DOM aktualisieren
                const neuerOrdner = document.createElement('div');
                neuerOrdner.className = 'rezension-text';

                const text = document.createElement('p');
                text.textContent = data.beschreibung;
                neuerOrdner.appendChild(text);

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
