# 🚀 Démarrage rapide MQTT

## ⚡ 5 minutes pour commencer

### 1️⃣ Installer le broker MQTT

**Option A - Windows (Chocolatey):**
```powershell
choco install mosquitto
```

**Option B - Docker:**
```bash
docker run -d -p 1883:1883 --name mosquitto eclipse-mosquitto
```

**Option C - Windows (exe):**
Télécharger depuis https://mosquitto.org/download/

### 2️⃣ Démarrer le broker

```bash
mosquitto
```

Voir: `✓ mosquitto version X.X.X running`

### 3️⃣ Démarrer le listener Django

```bash
python manage.py mqtt_listener
```

Voir: `✓ Client MQTT connecté et en écoute...`

### 4️⃣ Envoyer des données (nouveau terminal)

```bash
python manage.py mqtt_publish --temp 25 --hum 60
```

Voir: `📤 Publié: T=25°C, H=60%`

### 5️⃣ Vérifier la BD

Les données doivent être dans la table `DHT_Dht11`

---

## 📡 Via l'API REST

### Vérifier le statut MQTT

```bash
curl http://localhost:8000/mqtt/status/
```

Réponse:
```json
{
  "connected": true,
  "broker": "localhost",
  "port": 1883,
  "client_id": "django-dht11-client",
  "topics": {...}
}
```

### Publier des données

```bash
curl -X POST http://localhost:8000/mqtt/publish/sensor/ \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25, "humidity": 60}'
```

### Publier un incident

```bash
curl -X POST http://localhost:8000/mqtt/publish/incident/1/
```

---

## 🧪 Simulateur de capteurs

```bash
python mqtt_sensor_simulator.py
```

Options:
- Simulation continue (5 min)
- Simulation alerte température
- Publication unique

---

## 📊 Topics MQTT

### Écouter tous les messages (monitoring)

```bash
mosquitto_sub -h localhost -t "dht11/#" -v
```

### Publier manuellement

```bash
mosquitto_pub -h localhost -t "dht11/sensor/data" \
  -m '{"temperature":25,"humidity":60}'
```

---

## ✅ Vérifier l'intégration

### 1. Listener en cours d'exécution?
```bash
python manage.py mqtt_listener
```
Doit afficher: `✓ Connecté au broker MQTT`

### 2. Broker accessible?
```bash
mosquitto_sub -h localhost -t "test" -t 1
```

### 3. BD mise à jour?
```bash
python manage.py shell
>>> from DHT.models import Dht11
>>> Dht11.objects.count()
```

---

## 🔗 Fichiers clés

- Configuration: [projet/settings.py](../projet/settings.py#L119)
- Client MQTT: [DHT/mqtt_client.py](../DHT/mqtt_client.py)
- API REST: [DHT/api.py](../DHT/api.py#L210)
- Commandes: `DHT/management/commands/`
- Simulateur: [mqtt_sensor_simulator.py](../mqtt_sensor_simulator.py)

---

## 📚 Ressources

- [Guide complet](./MQTT_INTEGRATION_GUIDE.md)
- [Documentation paho-mqtt](https://github.com/eclipse/paho.mqtt.python)
- [Test avec curl](../EXAMPLES_CURL.sh)

---

## 🆘 Problèmes courants

**"Connection refused"**
```bash
# Vérifier que le broker est en cours d'exécution
mosquitto -v
```

**"No module named paho"**
```bash
pip install paho-mqtt
```

**Aucune donnée dans la BD**
- Le listener est-il actif?
- Les données sont-elles publiées?
- Y a-t-il des erreurs console?

**Topics ne reçoivent pas**
```bash
# Tester l'import MQTT
mosquitto_pub -h localhost -t "dht11/sensor/data" -m '{"temperature":20,"humidity":50}'
mosquitto_sub -h localhost -t "dht11/#" -v
```

---

**Besoin d'aide?** Voir [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md)
