let tempChart = null;

async function loadTempHistory(days = 1) {
    try {
        const res = await fetch("/api/");
        const allData = await res.json();

        // Filtrer par période
        const now = new Date();
        const cutoff = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
        
        const filteredData = allData.filter(row => {
            const rowDate = new Date(row.dt);
            return rowDate >= cutoff;
        });

        // Format date + heure précises
        const labels = filteredData.map(row => {
            const date = new Date(row.dt);
            return date.toLocaleString('fr-FR', {
                year: '2-digit',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        });
        const temps = filteredData.map(row => row.temp);

        // Détruire le graphique précédent
        if (tempChart) {
            tempChart.destroy();
        }

        const ctx = document.getElementById("tempChart");
        tempChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Température (°C)",
                    data: temps,
                    borderColor: "red",
                    borderWidth: 2,
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    x: {
                        display: true,
                        ticks: {
                            maxRotation: 45,
                            minRotation: 0,
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Température (°C)'
                        }
                    }
                }
            }
        });
    } catch (e) {
        console.error("Erreur API / graphe", e);
    }
}

// Charger par défaut 24h
loadTempHistory(1);

// Fonctions pour les boutons de période
function loadTemp24h() { loadTempHistory(1); }
function loadTemp7j() { loadTempHistory(7); }
function loadTemp30j() { loadTempHistory(30); }
