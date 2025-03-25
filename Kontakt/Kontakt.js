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
});

