"""
Service MQTT pour intégration du protocole MQTT avec le système d'incidents DHT11
"""
try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False

import json
import logging
from datetime import datetime
from django.conf import settings
from .models import Incident, Dht11

logger = logging.getLogger(__name__)


class MQTTClient:
    """Client MQTT pour gérer la connexion et les messages"""
    
    def __init__(self):
        if not MQTT_AVAILABLE:
            logger.warning("⚠️ paho-mqtt n'est pas installé. Installez-le avec: pip install paho-mqtt")
        
        self.client = None
        self.connected = False
        self.broker_address = getattr(settings, 'MQTT_BROKER_ADDRESS', 'localhost')
        self.broker_port = getattr(settings, 'MQTT_BROKER_PORT', 1883)
        self.client_id = getattr(settings, 'MQTT_CLIENT_ID', 'django-dht11-client')
        self.username = getattr(settings, 'MQTT_USERNAME', None)
        self.password = getattr(settings, 'MQTT_PASSWORD', None)
        
        # Topics MQTT
        self.topic_sensor_data = getattr(settings, 'MQTT_TOPIC_SENSOR_DATA', 'dht11/sensor/data')
        self.topic_incidents = getattr(settings, 'MQTT_TOPIC_INCIDENTS', 'dht11/incidents')
        self.topic_alerts = getattr(settings, 'MQTT_TOPIC_ALERTS', 'dht11/alerts')
        self.topic_status = getattr(settings, 'MQTT_TOPIC_STATUS', 'dht11/status')
        
    def setup(self):
        """Initialiser le client MQTT"""
        if not MQTT_AVAILABLE:
            logger.error("❌ paho-mqtt n'est pas installé. Installez-le avec: pip install paho-mqtt")
            return False
        
        try:
            self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv311)
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            # Authentification si configurée
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            
            logger.info(f"Connexion au broker MQTT: {self.broker_address}:{self.broker_port}")
            self.client.connect(self.broker_address, self.broker_port, keepalive=60)
            self.client.loop_start()
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la connexion MQTT: {str(e)}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback appelé quand le client se connecte"""
        if rc == 0:
            self.connected = True
            logger.info("✓ Connecté au broker MQTT")
            
            # S'abonner aux topics
            client.subscribe(self.topic_sensor_data)
            client.subscribe(self.topic_incidents)
            logger.info(f"Abonné aux topics: {self.topic_sensor_data}, {self.topic_incidents}")
            
            # Publier le statut
            self.publish_status("online")
        else:
            logger.error(f"Erreur de connexion MQTT (code: {rc})")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback appelé quand le client se déconnecte"""
        if rc != 0:
            logger.warning(f"Déconnexion inattendue du broker MQTT (code: {rc})")
        else:
            logger.info("Déconnecté du broker MQTT")
        self.connected = False
    
    def on_message(self, client, userdata, msg):
        """Callback appelé quand un message MQTT est reçu"""
        try:
            topic = msg.topic
            payload = msg.payload.decode()
            
            logger.debug(f"Message MQTT reçu - Topic: {topic}, Payload: {payload}")
            
            if topic == self.topic_sensor_data:
                self.handle_sensor_data(payload)
            elif topic == self.topic_incidents:
                self.handle_incident_data(payload)
                
        except Exception as e:
            logger.error(f"Erreur en traitant le message MQTT: {str(e)}")
    
    def handle_sensor_data(self, payload):
        """Traiter les données de capteur reçues via MQTT"""
        try:
            data = json.loads(payload)
            
            temp = data.get('temperature')
            hum = data.get('humidity')
            
            if temp is not None and hum is not None:
                # Créer un enregistrement DHT11
                dht_record = Dht11.objects.create(temp=temp, hum=hum)
                logger.info(f"Données capteur sauvegardées: T={temp}°C, H={hum}%")
                
                # Vérifier les seuils d'incidents
                self.check_incident_thresholds(temp, hum)
                
        except json.JSONDecodeError as e:
            logger.error(f"Erreur JSON dans les données capteur: {str(e)}")
    
    def handle_incident_data(self, payload):
        """Traiter les données d'incidents reçues via MQTT"""
        try:
            data = json.loads(payload)
            action = data.get('action')
            
            if action == 'create':
                incident = Incident.objects.create(
                    max_temp=data.get('max_temp', 0),
                    min_temp=data.get('min_temp', 0),
                    max_hum=data.get('max_hum', 0),
                    escalation_level=data.get('escalation_level', 0),
                    reason=data.get('reason', 'Créé via MQTT')
                )
                logger.info(f"Incident créé via MQTT (ID: {incident.id})")
                self.publish_incident_alert(incident)
                
            elif action == 'resolve':
                incident_id = data.get('incident_id')
                try:
                    incident = Incident.objects.get(id=incident_id)
                    incident.is_open = False
                    incident.status = 'resolved'
                    incident.save()
                    logger.info(f"Incident {incident_id} résolu via MQTT")
                except Incident.DoesNotExist:
                    logger.warning(f"Incident {incident_id} non trouvé")
                    
        except json.JSONDecodeError as e:
            logger.error(f"Erreur JSON dans les données d'incidents: {str(e)}")
    
    def check_incident_thresholds(self, temp, hum, temp_min=5, temp_max=35, hum_min=20, hum_max=80):
        """Vérifier si les seuils d'alerte sont dépassés"""
        if temp < temp_min or temp > temp_max or hum < hum_min or hum > hum_max:
            # Vérifier s'il y a déjà un incident ouvert
            open_incident = Incident.objects.filter(is_open=True).first()
            
            if not open_incident:
                incident = Incident.objects.create(
                    max_temp=temp if temp > 0 else 0,
                    min_temp=temp if temp > 0 else 0,
                    max_hum=hum,
                    reason=f"Dépassement des seuils: T={temp}°C, H={hum}%"
                )
                logger.warning(f"Incident créé automatiquement (ID: {incident.id})")
                self.publish_incident_alert(incident)
    
    def publish_sensor_data(self, temp, hum):
        """Publier les données de capteur"""
        if not self.connected:
            logger.warning("Client MQTT non connecté, publication impossible")
            return False
        
        payload = json.dumps({
            'temperature': temp,
            'humidity': hum,
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            result = self.client.publish(self.topic_sensor_data, payload, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Données capteur publiées: {payload}")
                return True
            else:
                logger.error(f"Erreur publication MQTT (code: {result.rc})")
                return False
        except Exception as e:
            logger.error(f"Erreur lors de la publication: {str(e)}")
            return False
    
    def publish_incident(self, incident):
        """Publier un incident"""
        if not self.connected:
            logger.warning("Client MQTT non connecté, publication impossible")
            return False
        
        payload = json.dumps({
            'incident_id': incident.id,
            'status': incident.status,
            'escalation_level': incident.escalation_level,
            'max_temp': float(incident.max_temp),
            'min_temp': float(incident.min_temp),
            'max_hum': float(incident.max_hum),
            'timestamp': incident.start_at.isoformat()
        })
        
        try:
            result = self.client.publish(self.topic_incidents, payload, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Incident publié: {payload}")
                return True
            else:
                logger.error(f"Erreur publication MQTT (code: {result.rc})")
                return False
        except Exception as e:
            logger.error(f"Erreur lors de la publication: {str(e)}")
            return False
    
    def publish_incident_alert(self, incident):
        """Publier une alerte d'incident"""
        if not self.connected:
            return False
        
        payload = json.dumps({
            'incident_id': incident.id,
            'alert_type': 'incident_created',
            'escalation_level': incident.escalation_level,
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            self.client.publish(self.topic_alerts, payload, qos=1)
            logger.info(f"Alerte incident publiée: {incident.id}")
            return True
        except Exception as e:
            logger.error(f"Erreur publication alerte: {str(e)}")
            return False
    
    def publish_status(self, status):
        """Publier le statut du service"""
        if not self.connected:
            return False
        
        payload = json.dumps({
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            self.client.publish(self.topic_status, payload, retain=True, qos=1)
            logger.debug(f"Statut publié: {status}")
            return True
        except Exception as e:
            logger.error(f"Erreur publication statut: {str(e)}")
            return False
    
    def disconnect(self):
        """Déconnecter le client MQTT"""
        if self.client:
            self.publish_status("offline")
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Client MQTT déconnecté")
            self.connected = False


# Instance globale du client MQTT
mqtt_client = MQTTClient()
