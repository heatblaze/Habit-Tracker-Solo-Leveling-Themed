// Radar chart for stats using Chart.js
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('statsRadar');
    if (ctx) {
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: radarLabels,
                datasets: [{
                    label: 'Stats',
                    data: radarData,
                    backgroundColor: 'rgba(106, 224, 255, 0.2)',
                    borderColor: '#6be0ff',
                    pointBackgroundColor: '#a259ff',
                    pointBorderColor: '#fff',
                }]
            },
            options: {
                scale: {
                    angleLines: { color: '#333' },
                    grid: { color: '#333' },
                    pointLabels: { color: '#e0e6f0' },
                    ticks: { color: '#e0e6f0', backdropColor: '#181824' }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
});
