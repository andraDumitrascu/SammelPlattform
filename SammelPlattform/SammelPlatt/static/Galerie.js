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

    const neuerOrdner = document.createElement('div');
    neuerOrdner.className = 'ordner'; 
    
    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.className = 'ordner-name-input';
    nameInput.placeholder = 'Ordnername eingeben';
    nameInput.maxLength = 30;
    nameInput.autocomplete = 'off';
    nameInput.required = true;
    
    neuerOrdner.appendChild(nameInput);
    
    const bild = document.createElement('img');
    bild.src = "{% static 'Bilder/Ordner.png' %}"; 
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

    const ordnerContainer = document.getElementById('Ordner');
    ordnerContainer.appendChild(neuerOrdner);
}
