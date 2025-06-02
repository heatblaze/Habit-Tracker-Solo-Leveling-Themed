document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('color-toggle');

    toggleButton.addEventListener('click', function () {
        const rootStyles = document.documentElement.style;
        const currentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim();

        if (currentColor === '#3b82f6') {
            rootStyles.setProperty('--accent-color', '#a855f7'); // Purple
        } else {
            rootStyles.setProperty('--accent-color', '#3b82f6'); // Blue
        }
    });
});

