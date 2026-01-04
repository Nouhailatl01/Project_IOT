# 🎯 Cas d'usage MQTT avancés

## 1️⃣ Intégration avec des capteurs physiques réels

### Capteur DHT11 via Arduino/ESP32

**Code Arduino/ESP32:**
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// Configuration WiFi
const char* ssid = "VOTRE_WIFI";
const char* password = "VOTRE_MOT_DE_PASSE";

// Configuration MQTT
const char* mqtt_server = "192.168.1.100";  // IP du broker
const int mqtt_port = 1883;
const char* mqtt_client_id = "esp32_dht11_sensor";
const char* mqtt_topic = "dht11/sensor/data";

// Configuration DHT11
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Connexion WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connecté!");
  
  // Connexion MQTT
  client.setServer(mqtt_server, mqtt_port);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(mqtt_client_id)) {
      Serial.println("Connecté au broker MQTT");
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Lire les données du capteur
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Erreur lecture DHT11");
    return;
  }
  
  // Publier les données
  String payload = "{\"temperature\":" + String(temperature, 2) + 
                   ",\"humidity\":" + String(humidity, 2) + "}";
  
  client.publish(mqtt_topic, payload.c_str());
  Serial.println("Publié: " + payload);
  
  delay(10000);  // Publication toutes les 10 secondes
}
```

**Configuration de l'Arduino:**
1. Installer les librairies: `WiFi`, `PubSubClient`, `DHT`
2. Modifier: `VOTRE_WIFI`, `VOTRE_MOT_DE_PASSE`, IP du broker
3. Uploader le sketch

### Configuration du broker pour Arduino

```bash
# Vérifier la connexion
mosquitto_sub -h localhost -t "dht11/#" -v

# Vous devriez voir les publications
dht11/sensor/data {"temperature":24.50,"humidity":65.30}
```

---

## 2️⃣ Intégration avec Home Assistant

### Configuration Home Assistant

**`configuration.yaml`:**
```yaml
mqtt:
  broker: localhost
  port: 1883

sensor:
  - platform: mqtt
    name: "Température DHT11"
    state_topic: "dht11/sensor/data"
    unit_of_measurement: "°C"
    value_template: "{{ value_json.temperature }}"
    
  - platform: mqtt
    name: "Humidité DHT11"
    state_topic: "dht11/sensor/data"
    unit_of_measurement: "%"
    value_template: "{{ value_json.humidity }}"

automation:
  - alias: "Alerte température basse"
    trigger:
      platform: numeric_state
      entity_id: sensor.temperature_dht11
      below: 5
    action:
      service: notify.telegram
      data:
        message: "Alerte: Température trop basse!"
```

---

## 3️⃣ Système de notifications temps réel

### WebSocket avec Django Channels (Futur)

```python
# channels_config.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MQTTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("mqtt_alerts", self.channel_name)
        await self.accept()
    
    async def mqtt_alert(self, event):
        """Envoyer une alerte MQTT au WebSocket"""
        await self.send(text_data=json.dumps(event['message']))
```

---

## 4️⃣ Persistance des données MQTT

### Historique complet

```python
# models.py - Ajouter ce modèle
class MQTTMessage(models.Model):
    topic = models.CharField(max_length=255)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-received_at']
    
    def __str__(self):
        return f"{self.topic} @ {self.received_at}"
```

### Mise à jour du client MQTT

```python
# mqtt_client.py - Dans on_message()
def on_message(self, client, userdata, msg):
    try:
        # Sauvegarder le message brut
        MQTTMessage.objects.create(
            topic=msg.topic,
            payload=json.loads(msg.payload.decode())
        )
        
        # Traiter le message
        topic = msg.topic
        payload = msg.payload.decode()
        # ... reste du code ...
```

---

## 5️⃣ Alertes escalade via MQTT

### Publication d'alertes d'escalade

```python
# Dans signals.py - Après escalade
def escalate_incident(incident, new_level):
    mqtt_client.publish_incident_alert(incident)
    
    # Publier une alerte spécifique
    alert_payload = {
        'incident_id': incident.id,
        'event': 'escalation',
        'from_level': incident.escalation_level,
        'to_level': new_level,
        'timestamp': datetime.now().isoformat()
    }
    
    mqtt_client.client.publish(
        'dht11/alerts/escalation',
        json.dumps(alert_payload),
        qos=1
    )
```

### Abonnement côté opérateurs

```bash
# Opérateur 1 s'abonne aux escalations
mosquitto_sub -t "dht11/alerts/escalation" -F "@Y-@m-@d @H:@M:@S | %p"
```

---

## 6️⃣ Règles conditionnelles MQTT

### Automatisation basée sur topics

```python
# mqtt_client.py - Ajouter dans on_message()
def handle_custom_rules(self, topic, payload):
    """Exécuter des règles personnalisées"""
    
    if topic == 'dht11/sensor/data':
        data = json.loads(payload)
        temp = data.get('temperature')
        
        # Règle 1: Alerte si température < 5°C pendant 5 mesures
        # Règle 2: Escalade d'office si température < 0°C
        if temp < 0:
            self.escalade_automatique()
        
        # Règle 3: Notification Slack si humidité > 90%
        if data.get('humidity', 0) > 90:
            self.send_slack_notification(data)
```

---

## 7️⃣ Intégration avec des services externes

### Envoyer vers InfluxDB

```python
from influxdb import InfluxDBClient

# mqtt_client.py
def send_to_influxdb(self, temp, humidity):
    client = InfluxDBClient(host='localhost', port=8086)
    
    json_body = [
        {
            "measurement": "dht11",
            "tags": {"location": "server_room"},
            "fields": {
                "temperature": temp,
                "humidity": humidity
            }
        }
    ]
    
    client.write_points(json_body)
```

### Envoyer vers Graphite

```python
import socket

def send_to_graphite(self, temp, humidity):
    sock = socket.socket()
    sock.connect(('localhost', 2003))
    
    metric_temp = f"dht11.temperature {temp} {int(time.time())}\n"
    metric_hum = f"dht11.humidity {humidity} {int(time.time())}\n"
    
    sock.sendall(metric_temp.encode())
    sock.sendall(metric_hum.encode())
    sock.close()
```

---

## 8️⃣ Clustering et haute disponibilité

### Configuration Mosquitto avec plusieurs brokers

```conf
# /etc/mosquitto/mosquitto.conf

# Broker 1
connection_messages true
log_dest file /var/log/mosquitto/mosquitto.log

# Bridge vers Broker 2
connection bridge_broker2
address broker2.example.com:1883
clientid bridge_broker1_to_broker2
topic dht11/# both

# Persistance
persistence true
persistence_location /var/lib/mosquitto/
```

### Client Django avec fallback

```python
# mqtt_client.py
BROKER_ADDRESSES = [
    ('broker1.example.com', 1883),
    ('broker2.example.com', 1883),
    ('localhost', 1883)  # Fallback local
]

def connect_with_fallback(self):
    for broker, port in BROKER_ADDRESSES:
        try:
            self.client.connect(broker, port, keepalive=60)
            self.broker_address = broker
            return True
        except:
            continue
    return False
```

---

## 9️⃣ Monitoring et métriques MQTT

### Dashboard Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'mqtt'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
```

### Exporter MQTT custom

```python
from prometheus_client import Counter, Gauge, start_http_server

mqtt_messages_received = Counter('mqtt_messages_total', 'Total MQTT messages')
mqtt_temperature = Gauge('mqtt_temperature_celsius', 'Current temperature')
mqtt_humidity = Gauge('mqtt_humidity_percent', 'Current humidity')

# Dans on_message()
mqtt_messages_received.inc()
if topic == 'dht11/sensor/data':
    data = json.loads(payload)
    mqtt_temperature.set(data.get('temperature'))
    mqtt_humidity.set(data.get('humidity'))
```

---

## 🔟 Sécurité avancée MQTT

### TLS/SSL avec certificats

```python
# mqtt_client.py
import ssl

def setup_tls(self):
    ca_certs = "/path/to/ca.crt"
    certfile = "/path/to/client.crt"
    keyfile = "/path/to/client.key"
    
    self.client.tls_set(
        ca_certs=ca_certs,
        certfile=certfile,
        keyfile=keyfile,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2,
        ciphers=None
    )
    self.client.tls_insecure_set(False)
```

### ACL (Access Control List) Mosquitto

```conf
# /etc/mosquitto/acl.txt

user django
topic read dht11/sensor/data
topic write dht11/incidents

user sensor
topic write dht11/sensor/data

user operator
topic read dht11/#
topic write dht11/incidents/response
```

---

## 📊 Statistiques et performance

### Monitoring des messages

```python
class MQTTMetrics:
    def __init__(self):
        self.messages_received = 0
        self.messages_published = 0
        self.errors = 0
        self.last_message_time = None
    
    def get_stats(self):
        return {
            'total_received': self.messages_received,
            'total_published': self.messages_published,
            'errors': self.errors,
            'last_message': self.last_message_time,
            'uptime_minutes': self.calculate_uptime()
        }
```

---

## 🔗 Ressources additionnelles

- [MQTT 3.1.1 Specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/)
- [Mosquitto Bridge Documentation](https://mosquitto.org/man/mosquitto-conf-5.html)
- [Home Assistant MQTT](https://www.home-assistant.io/integrations/mqtt/)
- [InfluxDB MQTT Bridge](https://github.com/influxdata/telegraf)

---

**Créé le:** 4 janvier 2026
