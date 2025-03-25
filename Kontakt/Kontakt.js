document.getElementById("teilenButton").addEventListener("click", function() {
    const zahl1 = parseFloat(document.getElementById("zahl1").value);
    const zahl2 = parseFloat(document.getElementById("zahl2").value);
    const ergebnisElement = document.getElementById("ergebnis");

    if (isNaN(zahl1) || isNaN(zahl2)) {
        ergebnisElement.textContent = "Bitte gültige Zahlen eingeben.";
        return;
    }

    if (zahl2 === 0) {
        ergebnisElement.textContent = "Fehler: Division durch 0 ist nicht erlaubt.";
        return;
    }

    const ergebnis = zahl1 / zahl2;
    ergebnisElement.textContent = `Ergebnis: ${ergebnis}`;

    createAnimatedPoints();
});

function createAnimatedPoints() {
    for (let i = 0; i < 5; i++) {
        const point = document.createElement('div');
        point.classList.add('animated-point');

        point.style.top = `${Math.random() * window.innerHeight}px`;
        point.style.left = `${Math.random() * window.innerWidth}px`;

        document.body.appendChild(point);

        setTimeout(() => {
            point.remove();
        }, 1000);  
    }
}
