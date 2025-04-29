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
    const neuerOrdner = document.createElement('div');
    neuerOrdner.className = 'ordner'; 

    const bild = document.createElement('img');
    bild.src = '../Bilder/Ordner.png'; 
    bild.alt = 'Ordnerbild'; 
    bild.className = 'ordner-bild'; 
    bild.style.width = '200px';


    neuerOrdner.appendChild(bild);

    const ordnerContainer = document.getElementById('Ordner');
    ordnerContainer.appendChild(neuerOrdner);
}