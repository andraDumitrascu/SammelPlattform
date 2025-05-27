// 🌙 Dark Mode Umschalten und Speichern
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }

    // 🧠 Login-Form Handler nur wenn Element vorhanden ist
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const baseURL = window.location.origin;
            const response = await fetch(`${baseURL}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.message || 'Login erfolgreich!');
                window.location.href = '/galerie/';  // ✅ Zur Galerie weiterleiten
            } else {
                const errorData = await response.json();
                alert(errorData.error || 'Login fehlgeschlagen');
            }
        });
    }
});
