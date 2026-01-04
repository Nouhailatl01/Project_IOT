"""
Management command pour publier des données de test via MQTT
Utilisation: python manage.py mqtt_publish --temp 25 --hum 60
"""
from django.core.management.base import BaseCommand
from DHT.mqtt_client import mqtt_client
import time


class Command(BaseCommand):
    help = 'Publie des données de test via MQTT'

    def add_arguments(self, parser):
        parser.add_argument(
            '--temp',
            type=float,
            help='Température à publier'
        )
        parser.add_argument(
            '--hum',
            type=float,
            help='Humidité à publier'
        )
        parser.add_argument(
            '--incident',
            type=int,
            help='ID d\'incident à publier'
        )

    def handle(self, *args, **options):
        # Initialiser le client
        if not mqtt_client.setup():
            self.stdout.write(
                self.style.ERROR('✗ Impossible de se connecter au broker MQTT')
            )
            return
        
        # Attendre la connexion
        time.sleep(2)
        
        # Publier les données de capteur
        if options.get('temp') is not None and options.get('hum') is not None:
            temp = options.get('temp')
            hum = options.get('hum')
            
            if mqtt_client.publish_sensor_data(temp, hum):
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Données publiées: T={temp}°C, H={hum}%')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('✗ Erreur lors de la publication')
                )
        
        # Publier l'incident
        if options.get('incident'):
            from DHT.models import Incident
            incident_id = options.get('incident')
            
            try:
                incident = Incident.objects.get(id=incident_id)
                if mqtt_client.publish_incident(incident):
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Incident {incident_id} publié')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('✗ Erreur lors de la publication')
                    )
            except Incident.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Incident {incident_id} non trouvé')
                )
        
        # Attendre un peu avant de déconnecter
        time.sleep(1)
        mqtt_client.disconnect()
