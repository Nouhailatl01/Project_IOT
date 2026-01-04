"""
Exemple de script pour publier des données de capteur via MQTT
Permet de simuler des capteurs DHT11 qui publient des données via MQTT
"""
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime


class DHTSimulator:
    """Simulateur de capteur DHT11"""
    
    def __init__(self, broker='localhost', port=1883, topic='dht11/sensor/data'):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = None
        self.connected = False
    
    def connect(self):
        """Se connecter au broker MQTT"""
        self.client = mqtt.Client(client_id='dht11-simulator')
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            time.sleep(2)  # Attendre la connexion
            return self.connected
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"✓ Connecté au broker MQTT ({self.broker}:{self.port})")
        else:
            print(f"❌ Erreur de connexion (code: {rc})")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc != 0:
            print(f"⚠️ Déconnexion inattendue (code: {rc})")
    
    def publish_data(self, temp, humidity):
        """Publier les données de capteur"""
        if not self.connected:
            print("⚠️ Non connecté au broker")
            return False
        
        payload = json.dumps({
            'temperature': temp,
            'humidity': humidity,
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            result = self.client.publish(self.topic, payload, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"📤 Publié: T={temp}°C, H={humidity}% [{datetime.now().strftime('%H:%M:%S')}]")
                return True
            return False
        except Exception as e:
            print(f"❌ Erreur publication: {e}")
            return False
    
    def publish_random_data(self, temp_base=25, temp_range=5, hum_base=60, hum_range=10):
        """Publier des données aléatoires (simulation)"""
        temp = temp_base + random.uniform(-temp_range, temp_range)
        humidity = hum_base + random.uniform(-hum_range, hum_range)
        humidity = max(0, min(100, humidity))  # Limiter à 0-100%
        return self.publish_data(round(temp, 2), round(humidity, 2))
    
    def simulate_continuous(self, duration=300, interval=10):
        """Simuler les données pendant une durée spécifiée"""
        print(f"\n🔄 Simulation continue: {duration}s, publication tous les {interval}s")
        print("=" * 50)
        
        start_time = time.time()
        count = 0
        
        try:
            while time.time() - start_time < duration:
                self.publish_random_data()
                count += 1
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n⏹️ Simulation arrêtée par l'utilisateur")
        
        print("=" * 50)
        print(f"✓ Simulation terminée: {count} publications")
        self.disconnect()
    
    def simulate_temperature_alert(self):
        """Simuler une alerte de température"""
        print("\n🔄 Simulation alerte température")
        print("=" * 50)
        
        # Température normale
        for i in range(3):
            print(f"[{i+1}/3] Température normale...")
            self.publish_data(25, 60)
            time.sleep(2)
        
        # Température basse (alerte)
        print("\n⚠️ Abaissement de température...")
        for temp in [20, 15, 10, 5, 3]:
            self.publish_data(temp, 60)
            time.sleep(2)
        
        # Remonter
        print("\n📈 Remontée de température...")
        for temp in [8, 12, 18, 25]:
            self.publish_data(temp, 60)
            time.sleep(2)
        
        print("\n✓ Simulation alerte terminée")
        print("=" * 50)
        self.disconnect()
    
    def disconnect(self):
        """Déconnecter du broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            print("✓ Déconnecté du broker MQTT")


if __name__ == '__main__':
    # Configuration
    BROKER = 'localhost'  # Modifier si le broker est sur une autre machine
    PORT = 1883
    TOPIC = 'dht11/sensor/data'
    
    # Créer le simulateur
    sim = DHTSimulator(broker=BROKER, port=PORT, topic=TOPIC)
    
    # Se connecter
    if sim.connect():
        # Option 1: Simulation continue (5 minutes, publication toutes les 10 secondes)
        # sim.simulate_continuous(duration=300, interval=10)
        
        # Option 2: Simuler une alerte de température
        sim.simulate_temperature_alert()
        
        # Option 3: Publication unique
        # sim.publish_data(temp=25, humidity=60)
        # sim.disconnect()
    else:
        print("❌ Impossible de se connecter au broker MQTT")
        print("Assurez-vous que le broker MQTT est en cours d'exécution")
