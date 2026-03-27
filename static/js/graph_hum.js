let humChart = null;

async function loadHumHistory(days = 1) {
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
        const hums = filteredData.map(row => row.hum);

        // Détruire le graphique précédent
        if (humChart) {
            humChart.destroy();
        }

        const ctx = document.getElementById("humChart");
        humChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Humidité (%)",
                    data: hums,
                    borderColor: "blue",
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
                            text: 'Humidité (%)'
                        }
                    }
                }
            }
        });
    } catch (e) {
        console.error("Erreur API / graphe humidité", e);
    }
}

// Charger par défaut 24h
loadHumHistory(1);

// Fonctions pour les boutons de période
function loadHum24h() { loadHumHistory(1); }
function loadHum7j() { loadHumHistory(7); }
function loadHum30j() { loadHumHistory(30); }
