function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});

document.getElementById('login-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

   const baseURL = window.location.origin;
const response = await fetch(`${baseURL}/login/`, {  // changed here
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
});



    if (response.ok) {
        alert('Login erfolgreich!');
        window.location.href = '/';
    } else {
        alert('Login fehlgeschlagen');
        window.location.href = '/login/';
    }
});