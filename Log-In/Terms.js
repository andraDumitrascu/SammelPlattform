document.addEventListener("DOMContentLoaded", function() {
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
