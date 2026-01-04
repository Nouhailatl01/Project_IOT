# 🚀 Guide d'Intégration MQTT

## 📋 Vue d'ensemble

L'intégration MQTT permet à votre système Django de communiquer avec des capteurs DHT11 et d'autres appareils IoT via le protocole MQTT. MQTT est un protocole léger idéal pour les applications IoT.

### Caractéristiques

✅ **Publication/Abonnement** aux données de capteurs  
✅ **Gestion automatique des incidents** via MQTT  
✅ **Alertes en temps réel**  
✅ **Persistence des messages** (QoS 1)  
✅ **Support d'authentification**  
✅ **Simulateur de capteurs inclus**  

---

## 📦 Installation

### 1. Dépendances

La bibliothèque `paho-mqtt` a déjà été installée. Pour vérifier:

```bash
pip list | grep paho
```

### 2. Configuration Django

Les paramètres MQTT sont définis dans [projet/settings.py](../projet/settings.py):

```python
# Configuration du broker
MQTT_BROKER_ADDRESS = 'localhost'       # Adresse du broker
MQTT_BROKER_PORT = 1883                 # Port MQTT
MQTT_CLIENT_ID = 'django-dht11-client'  # ID du client

# Seuils d'alerte
MQTT_TEMP_MIN = 5
MQTT_TEMP_MAX = 35
MQTT_HUM_MIN = 20
MQTT_HUM_MAX = 80

# Topics MQTT
MQTT_TOPIC_SENSOR_DATA = 'dht11/sensor/data'
MQTT_TOPIC_INCIDENTS = 'dht11/incidents'
MQTT_TOPIC_ALERTS = 'dht11/alerts'
MQTT_TOPIC_STATUS = 'dht11/status'
```

### 3. Authentification (Optionnel)

Pour un broker avec authentification:

```python
# Dans settings.py
MQTT_USERNAME = 'votre_utilisateur'
MQTT_PASSWORD = 'votre_mot_de_passe'
```

---

## 🔧 Architecture

### Fichiers créés

| Fichier | Description |
|---------|-------------|
| [DHT/mqtt_client.py](../DHT/mqtt_client.py) | Client MQTT principal |
| [DHT/management/commands/mqtt_listener.py](../DHT/management/commands/mqtt_listener.py) | Commande pour démarrer le service |
| [DHT/management/commands/mqtt_publish.py](../DHT/management/commands/mqtt_publish.py) | Commande pour publier des données |
| [mqtt_sensor_simulator.py](../mqtt_sensor_simulator.py) | Simulateur de capteurs |

### Flux de données

```
┌─────────────────────────────────────────────────────────────┐
│                    MQTT Broker                              │
│  (Serveur MQTT central)                                     │
└─────────────┬───────────────────────────────────┬───────────┘
              │                                   │
              ▼                                   ▼
    ┌──────────────────┐              ┌──────────────────┐
    │  Capteurs IoT    │              │  Django App      │
    │  (DHT11)         │◄────────────►│  (Listener)      │
    │  ou Simulateur   │              │                  │
    └──────────────────┘              └────────┬─────────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ Base de      │
                                        │ données      │
                                        │ (Incidents)  │
                                        └──────────────┘
```

---

## 🎯 Utilisation

### 1. Installation d'un broker MQTT

Vous devez avoir un broker MQTT en cours d'exécution. Plusieurs options:

#### Option A: Mosquitto (Recommandé)

**Windows:**
```powershell
# Installer via Chocolatey
choco install mosquitto

# Ou télécharger depuis: https://mosquitto.org/download/
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install mosquitto mosquitto-clients

# macOS
brew install mosquitto
```

**Démarrer le broker:**
```bash
mosquitto -v
```

#### Option B: Docker

```bash
docker run -d -p 1883:1883 --name mosquitto eclipse-mosquitto
```

#### Option C: Broker en ligne (test)

```python
# Dans settings.py
MQTT_BROKER_ADDRESS = 'broker.emqx.io'  # Broker public EMQX
```

### 2. Démarrer le service MQTT

Une fois le broker en cours d'exécution:

```bash
python manage.py mqtt_listener
```

Résultat attendu:
```
✓ Client MQTT connecté et en écoute...
Abonné aux topics: dht11/sensor/data, dht11/incidents
```

### 3. Publier des données

#### A. Via la ligne de commande

```bash
# Publier les données de capteur
python manage.py mqtt_publish --temp 25 --hum 60

# Publier un incident
python manage.py mqtt_publish --incident 1
```

#### B. Via le simulateur

```bash
python mqtt_sensor_simulator.py
```

Le simulateur offre plusieurs options:

- **Simulation continue** (5 min, toutes les 10s)
- **Simulation d'alerte température** (baisse progressive)
- **Publication unique**

#### C. Via l'API Django

```python
from DHT.mqtt_client import mqtt_client

# Publier des données de capteur
mqtt_client.publish_sensor_data(temp=25, hum=60)

# Publier un incident
from DHT.models import Incident
incident = Incident.objects.get(id=1)
mqtt_client.publish_incident(incident)
```

---

## 📡 Topics MQTT

### Topics de souscription (Django écoute)

| Topic | Format | Description |
|-------|--------|-------------|
| `dht11/sensor/data` | `{"temperature": 25.5, "humidity": 60}` | Données des capteurs |
| `dht11/incidents` | `{"action": "create", ...}` | Gestion des incidents |

### Topics de publication (Django publie)

| Topic | Format | Description |
|-------|--------|-------------|
| `dht11/incidents` | `{"incident_id": 1, "status": "open", ...}` | État des incidents |
| `dht11/alerts` | `{"incident_id": 1, "alert_type": "..."}` | Alertes en temps réel |
| `dht11/status` | `{"status": "online"}` | Statut du service |

---

## 🧪 Scénarios de test

### Scénario 1: Publication de données normales

```bash
# Terminal 1: Démarrer le listener
python manage.py mqtt_listener

# Terminal 2: Publier des données
python manage.py mqtt_publish --temp 25 --hum 60
```

**Résultat:** Les données sont sauvegardées dans la BD, pas d'incident.

### Scénario 2: Alerte température basse

```bash
# Terminal 1: Listener en cours d'exécution

# Terminal 2: Publier température basse
python manage.py mqtt_publish --temp 3 --hum 60
```

**Résultat:** 
- ❌ Incident créé automatiquement
- 📧 Email d'alerte envoyé
- 📡 Publication via MQTT

### Scénario 3: Simulation complète

```bash
# Terminal 1: Listener
python manage.py mqtt_listener

# Terminal 2: Simulateur
python mqtt_sensor_simulator.py

# Choisir: Simulation d'alerte température
```

**Résultat:** Voir les incidents créés et résolus en temps réel.

---

## 📊 Monitoring

### Vérifier la connexion MQTT

```bash
# Terminal 1: S'abonner aux topics (pour monitoring)
mosquitto_sub -h localhost -t "dht11/#" -v

# Terminal 2: Publier des données
python manage.py mqtt_publish --temp 25 --hum 60
```

### Logs Django

Les logs sont enregistrés dans le système de logging Django. Pour activer les logs de debug:

```python
# Dans settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

---

## 🔐 Sécurité

### Développement

Les paramètres actuels conviennent pour le développement local.

### Production

#### 1. Authentification MQTT

```python
# settings.py
MQTT_USERNAME = 'mqtt_user'
MQTT_PASSWORD = 'secure_password'
```

#### 2. TLS/SSL

```python
# settings.py
MQTT_BROKER_PORT = 8883  # Port TLS
```

#### 3. Topics restreints

Configurer le broker pour limiter les accès par topic.

---

## 🐛 Dépannage

### Erreur: "Connection refused"

**Cause:** Le broker MQTT n'est pas en cours d'exécution.

**Solution:**
```bash
# Vérifier le statut du broker
mosquitto -v

# Ou utiliser Docker
docker run -d -p 1883:1883 eclipse-mosquitto
```

### Erreur: "No module named 'paho'"

**Solution:**
```bash
pip install paho-mqtt
```

### Les messages ne sont pas reçus

**Vérifier:**
1. Le broker est-il en cours d'exécution?
2. L'adresse/port du broker sont-ils corrects?
3. Le listener Django est-il en cours d'exécution?

```bash
# Tester la publication
mosquitto_pub -h localhost -t "dht11/sensor/data" -m '{"temperature":25,"humidity":60}'

# Vérifier la réception
mosquitto_sub -h localhost -t "dht11/#" -v
```

### La base de données n'est pas mise à jour

**Vérifier:**
1. Le listener Django affiche-t-il les logs?
2. Y a-t-il des erreurs dans la console?
3. Les migrations Django sont-elles appliquées?

```bash
python manage.py migrate
```

---

## 📚 Ressources

- [Documentation paho-mqtt](https://github.com/eclipse/paho.mqtt.python)
- [Protocole MQTT](https://mqtt.org/)
- [Mosquitto Documentation](https://mosquitto.org/documentation/)
- [EMQX Broker (Cloud MQTT)](https://www.emqx.com/)

---

## 🎯 Prochaines étapes

### Fonctionnalités à ajouter

- [ ] WebSocket MQTT pour le dashboard temps réel
- [ ] Système de topics à granularité multiple (par capteur)
- [ ] Historique des messages MQTT
- [ ] Alertes WebSocket au lieu d'email
- [ ] Commande pour configurer le broker dynamiquement
- [ ] Interface d'administration pour les topics

### Configuration avancée

- [ ] Support de plusieurs brokers
- [ ] Retry automatique avec backoff exponentiel
- [ ] Persistance des messages
- [ ] Clustering MQTT

---

**Créé le:** 4 janvier 2026  
**Dernière mise à jour:** 4 janvier 2026
