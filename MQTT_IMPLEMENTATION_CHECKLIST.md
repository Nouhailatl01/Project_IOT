# ✅ MQTT Integration Checklist

## 📋 Avant de commencer

- [ ] Lire [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md)
- [ ] Installer un broker MQTT (voir section Installation)
- [ ] Vérifier Python 3.9+ avec `python --version`

---

## 🔧 Installation & Configuration

### Broker MQTT

**Option 1: Windows avec Chocolatey**
```bash
choco install mosquitto
```
- [ ] Mosquitto installé
- [ ] Service démarré: `mosquitto -v`

**Option 2: Docker**
```bash
docker run -d -p 1883:1883 --name mosquitto eclipse-mosquitto
```
- [ ] Docker en cours d'exécution
- [ ] Port 1883 accessible

**Option 3: Broker en ligne**
```python
# settings.py
MQTT_BROKER_ADDRESS = 'broker.emqx.io'
```
- [ ] Configuration modifiée

### Dépendances Python

```bash
pip install paho-mqtt
```
- [ ] paho-mqtt 2.1.0+ installé
- [ ] Vérifier: `pip show paho-mqtt`

### Django

```bash
python manage.py check
```
- [ ] ✅ System check identified no issues

---

## 🚀 Démarrage du service

### Terminal 1: Listener MQTT
```bash
python manage.py mqtt_listener
```
- [ ] Message: `✓ Client MQTT connecté et en écoute...`
- [ ] Message: `Abonné aux topics: dht11/sensor/data, dht11/incidents`

### Terminal 2: Tests

#### Test 1: Publication manuelle
```bash
python manage.py mqtt_publish --temp 25 --hum 60
```
- [ ] Message: `📤 Publié: T=25°C, H=60%`
- [ ] Données apparaissent en BD

#### Test 2: Simulateur
```bash
python mqtt_sensor_simulator.py
```
- [ ] Sélectionner option
- [ ] Vérifier les messages publiés

#### Test 3: API REST
```bash
curl http://localhost:8000/mqtt/status/
```
- [ ] Réponse JSON avec status
- [ ] `"connected": true`

---

## 📡 Vérification des données

### Base de données
```bash
python manage.py shell
>>> from DHT.models import Dht11
>>> Dht11.objects.count()
# Doit être > 0 après publications
```
- [ ] Données présentes en BD

### MQTT Topics (Monitoring)
```bash
mosquitto_sub -h localhost -t "dht11/#" -v
```
- [ ] Reçoit les messages publiés
- [ ] Format JSON valide

### API Incidents
```bash
curl http://localhost:8000/incident/status/
```
- [ ] Incidents visibles si créés

---

## 🔒 Configuration Production

### Authentification

```python
# settings.py
MQTT_USERNAME = 'votre_user'
MQTT_PASSWORD = 'votre_mdp'
```
- [ ] Configuré si broker le requiert

### Seuils d'alerte

```python
# settings.py
MQTT_TEMP_MIN = 5
MQTT_TEMP_MAX = 35
MQTT_HUM_MIN = 20
MQTT_HUM_MAX = 80
```
- [ ] Ajustés pour votre cas

### TLS/SSL

```python
# settings.py
MQTT_BROKER_PORT = 8883  # Ou 8884, 8885
```
- [ ] Port TLS configuré

---

## 📚 Documentation

### Consultées
- [ ] [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md)
- [ ] [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md)
- [ ] [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md)

### Fonctionnalités comprises
- [ ] Publication de données capteur
- [ ] Création automatique d'incidents
- [ ] API REST disponible
- [ ] Simulateur de capteurs
- [ ] Topics MQTT

---

## 🧪 Scénarios de test

### Scénario 1: Données normales
```bash
python manage.py mqtt_publish --temp 25 --hum 60
```
- [ ] Pas d'incident créé
- [ ] Données en BD

### Scénario 2: Alerte temperature basse
```bash
python manage.py mqtt_publish --temp 2 --hum 60
```
- [ ] Incident créé automatiquement
- [ ] Email envoyé (vérifier logs)
- [ ] Alerte publiée via MQTT

### Scénario 3: Alerte humidité haute
```bash
python manage.py mqtt_publish --temp 25 --hum 95
```
- [ ] Incident créé automatiquement
- [ ] Message MQTT publié

### Scénario 4: Simulation complète
```bash
python mqtt_sensor_simulator.py
# Choisir: "Simulation d'alerte température"
```
- [ ] Incidents créés et résolus
- [ ] Logs affichés correctement

---

## 🔗 Intégrations additionnelles

### Arduino/ESP32 (optionnel)
- [ ] Sketch uploadé (voir MQTT_ADVANCED_CASES.md)
- [ ] Données reçues depuis l'appareil

### Home Assistant (optionnel)
- [ ] Configuration YAML ajoutée
- [ ] Capteurs visibles dans HA

### Grafana (optionnel)
- [ ] Dashboard créé
- [ ] Graphiques affichent les données

---

## 📊 Endpoints API REST

### Tester chaque endpoint

#### 1. Status
```bash
curl http://localhost:8000/mqtt/status/
```
- [ ] ✅ Retourne JSON

#### 2. Publish Sensor
```bash
curl -X POST http://localhost:8000/mqtt/publish/sensor/ \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25, "humidity": 60}'
```
- [ ] ✅ Retourne `{"success": true}`

#### 3. Publish Incident
```bash
curl -X POST http://localhost:8000/mqtt/publish/incident/1/
```
- [ ] ✅ Retourne `{"success": true}` ou 404 si pas d'incident

#### 4. Connect
```bash
curl -X POST http://localhost:8000/mqtt/connect/ \
  -H "Content-Type: application/json" \
  -d '{"broker": "localhost", "port": 1883}'
```
- [ ] ✅ Se connecte au broker

#### 5. Disconnect
```bash
curl -X POST http://localhost:8000/mqtt/disconnect/
```
- [ ] ✅ Se déconnecte

---

## 🐛 Dépannage

### Problème: "Connection refused"
- [ ] Broker MQTT en cours d'exécution?
  ```bash
  mosquitto -v
  ```
- [ ] Port 1883 accessible?
  ```bash
  telnet localhost 1883
  ```

### Problème: "No module named paho"
- [ ] Réinstaller:
  ```bash
  pip uninstall paho-mqtt && pip install paho-mqtt
  ```
- [ ] Bon venv activé?

### Problème: Aucune donnée en BD
- [ ] Listener en cours d'exécution?
- [ ] Données publiées?
  ```bash
  mosquitto_sub -t "dht11/sensor/data" -v
  ```
- [ ] Pas d'erreurs dans la console?

### Problème: Incidents non créés
- [ ] Données publiées dépassent les seuils?
- [ ] Vérifier les seuils dans settings.py

---

## ✅ Checklist finale

### Système fonctionnel
- [ ] Broker MQTT démarre sans erreur
- [ ] Django démarre (`manage.py check`)
- [ ] Listener écoute les topics
- [ ] Simulateur publie les données
- [ ] API REST répond
- [ ] Données apparaissent en BD
- [ ] Incidents créés si dépassement seuils
- [ ] Tous les logs sont clairs

### Documentation
- [ ] Guide complet lu
- [ ] Quickstart suivi
- [ ] Tous les endpoints testés
- [ ] Scénarios de test réussis

### Production-ready
- [ ] Configuration MQTT en place
- [ ] Authentification (optionnel)
- [ ] Seuils d'alerte ajustés
- [ ] TLS/SSL (si nécessaire)
- [ ] Monitoring configuré

---

## 🎉 Statut: READY FOR PRODUCTION

Votre système MQTT est maintenant **complètement intégré** et **opérationnel**.

### Prochaines étapes
1. Connecter vos capteurs réels
2. Configurer les alertes (email/Slack)
3. Mettre en place le monitoring
4. Tester en condition réelle

### Ressources
- Documentation: `MQTT_INTEGRATION_GUIDE.md`
- Exemples: `EXAMPLES_MQTT_API.sh`
- Code: `DHT/mqtt_client.py`

---

**Besoin d'aide?** Consultez la [Guide d'intégration](./MQTT_INTEGRATION_GUIDE.md)

**Date de completion:** 4 janvier 2026  
**Version:** 1.0 Final ✅
