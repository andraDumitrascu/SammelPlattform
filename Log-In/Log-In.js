function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
        document.body.classList.remove('light-mode');
    } else {
        localStorage.setItem('darkMode', 'disabled');
        document.body.classList.add('light-mode');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.add('light-mode');
    }
});

