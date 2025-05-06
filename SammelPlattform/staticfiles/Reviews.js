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
    hinzufuegenButton.onclick = function() {
        const rezensionText = eingabeFeld.value;
        if (rezensionText) {
            const neuerOrdner = document.createElement('div');
            neuerOrdner.className = 'rezension-text'; 

            const text = document.createElement('p');
            text.textContent = rezensionText;
            neuerOrdner.appendChild(text);

            const ordnerContainer = document.getElementById('rezension');
            ordnerContainer.appendChild(neuerOrdner);

            eingabeFeld.value = '';

            eingabeContainer.style.display = 'none';
        } else {
            alert('Bitte gib eine Rezension ein.');
        }
    };

    eingabeContainer.appendChild(eingabeFeld);
    eingabeContainer.appendChild(hinzufuegenButton);

    const ordnerContainer = document.getElementById('rezension');
    ordnerContainer.appendChild(eingabeContainer);
}
