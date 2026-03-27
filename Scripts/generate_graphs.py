import os

graph_temp = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <title>Graphique Température</title>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; padding: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
        h1 { margin-bottom: 25px; color: #333; }
        .back-btn { display: inline-block; margin-bottom: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 4px; font-weight: 600; }
        .back-btn:hover { background: #764ba2; }
        .filters { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 25px; padding: 20px; background: #f9f9f9; border-radius: 8px; }
        .filter-group { display: flex; flex-direction: column; gap: 5px; }
        .filter-group label { font-weight: 600; font-size: 12px; color: #666; }
        .filter-group input { padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .buttons { display: flex; gap: 10px; flex-wrap: wrap; }
        button { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
        button:hover { background: #764ba2; }
        button.green { background: #4CAF50; }
        button.green:hover { background: #45a049; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-card .value { font-size: 28px; font-weight: bold; }
        .stat-card .label { font-size: 12px; opacity: 0.9; margin-top: 5px; }
        #csvInput { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/dashboard/" class="back-btn">← Retour</a>
        <h1>📊 Graphique Température</h1>
        
        <div class="filters">
            <div class="filter-group">
                <label>Début</label>
                <input type="date" id="dateStart">
            </div>
            <div class="filter-group">
                <label>Fin</label>
                <input type="date" id="dateEnd">
            </div>
            <div class="buttons">
                <button onclick="filterData()">🔍 Filtrer</button>
                <button class="green" onclick="exportCSV()">📥 Exporter</button>
                <button class="green" onclick="document.getElementById('csvInput').click()">📤 Importer</button>
            </div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="label">Temp Min</div>
                <div class="value" id="minTemp">--</div>
            </div>
            <div class="stat-card">
                <div class="label">Temp Max</div>
                <div class="value" id="maxTemp">--</div>
            </div>
            <div class="stat-card">
                <div class="label">Temp Moy</div>
                <div class="value" id="avgTemp">--</div>
            </div>
            <div class="stat-card">
                <div class="label">Mesures</div>
                <div class="value" id="countTemp">0</div>
            </div>
        </div>

        <div id="tempChart"></div>
    </div>

    <input type="file" id="csvInput" accept=".csv" onchange="importCSV()">

    <script>
        let allData = [];
        let chart = null;

        async function loadData() {
            const response = await fetch('/api/');
            const data = await response.json();
            allData = data.results || [];
            filterData();
        }

        function filterData() {
            let filtered = allData;
            const startDate = document.getElementById('dateStart').value;
            const endDate = document.getElementById('dateEnd').value;

            if (startDate) {
                const start = new Date(startDate);
                filtered = filtered.filter(d => new Date(d.dt) >= start);
            }
            if (endDate) {
                const end = new Date(endDate);
                end.setHours(23, 59, 59, 999);
                filtered = filtered.filter(d => new Date(d.dt) <= end);
            }

            updateChart(filtered);
        }

        function updateChart(data) {
            if (!data || data.length === 0) {
                document.getElementById('minTemp').textContent = '--';
                document.getElementById('maxTemp').textContent = '--';
                document.getElementById('avgTemp').textContent = '--';
                document.getElementById('countTemp').textContent = '0';
                if (chart) chart.destroy();
                document.getElementById('tempChart').innerHTML = '<p style="text-align: center; padding: 40px; color: #999;">Aucune donnée</p>';
                return;
            }

            const temps = data.map(d => d.temp);
            const labels = data.map(d => new Date(d.dt).toLocaleString('fr-FR'));

            const min = Math.min(...temps).toFixed(1);
            const max = Math.max(...temps).toFixed(1);
            const avg = (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1);

            document.getElementById('minTemp').textContent = min + '°C';
            document.getElementById('maxTemp').textContent = max + '°C';
            document.getElementById('avgTemp').textContent = avg + '°C';
            document.getElementById('countTemp').textContent = data.length;

            const options = {
                series: [{name: 'Température (°C)', data: temps}],
                chart: {type: 'line', height: 400, toolbar: {show: true}},
                stroke: {curve: 'smooth', width: 3, colors: ['#667eea']},
                fill: {type: 'gradient', gradient: {shadeIntensity: 1, opacityFrom: 0.45, opacityTo: 0.05}},
                xaxis: {categories: labels},
                yaxis: {title: {text: 'Température (°C)'}},
                tooltip: {theme: 'dark'},
                grid: {show: true}
            };

            if (chart) chart.destroy();
            chart = new ApexCharts(document.getElementById('tempChart'), options);
            chart.render();
        }

        function exportCSV() {
            let csv = 'Date/Heure,Température (°C),Humidité (%)\\n';
            allData.forEach(d => {
                csv += `"${d.dt}",${d.temp},${d.hum}\\n`;
            });
            const link = document.createElement('a');
            link.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
            link.download = 'temperature_' + new Date().getTime() + '.csv';
            link.click();
        }

        function importCSV() {
            const file = document.getElementById('csvInput').files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                const csv = e.target.result;
                const lines = csv.trim().split('\\n');
                lines.slice(1).forEach(line => {
                    const parts = line.split(',');
                    if (parts.length >= 2) {
                        const temp = parseFloat(parts[1]);
                        if (!isNaN(temp)) {
                            fetch('/api/post', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({temp, hum: 0})
                            });
                        }
                    }
                });
                setTimeout(loadData, 1000);
            };
            reader.readAsText(file);
        }

        const today = new Date();
        const sevenDaysAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
        document.getElementById('dateStart').valueAsDate = sevenDaysAgo;
        document.getElementById('dateEnd').valueAsDate = today;
        loadData();
    </script>
</body>
</html>'''

graph_hum = graph_temp.replace('Température', 'Humidité').replace('temp', 'hum').replace('°C', '%').replace('#667eea', '#00BCD4')

with open('templates/graph_temp.html', 'w', encoding='utf-8') as f:
    f.write(graph_temp)
    
with open('templates/graph_hum.html', 'w', encoding='utf-8') as f:
    f.write(graph_hum)

print("✅ Fichiers graphes créés avec succès!")
