"""
Management command pour démarrer le client MQTT
Utilisation: python manage.py mqtt_listener
"""
from django.core.management.base import BaseCommand, CommandError
from DHT.mqtt_client import mqtt_client
import logging
import time
import signal
import sys

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Démarre le service client MQTT pour recevoir les données des capteurs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--broker',
            type=str,
            default='localhost',
            help='Adresse du broker MQTT (par défaut: localhost)'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=1883,
            help='Port du broker MQTT (par défaut: 1883)'
        )

    def handle(self, *args, **options):
        broker = options.get('broker')
        port = options.get('port')
        
        self.stdout.write(
            self.style.SUCCESS(f'Démarrage du service MQTT...')
        )
        self.stdout.write(
            self.style.WARNING(f'Broker: {broker}:{port}')
        )
        
        # Mettre à jour les paramètres si différents des defaults
        mqtt_client.broker_address = broker
        mqtt_client.broker_port = port
        
        # Initialiser le client
        if not mqtt_client.setup():
            raise CommandError('Impossible de se connecter au broker MQTT')
        
        self.stdout.write(
            self.style.SUCCESS('✓ Client MQTT connecté et en écoute...')
        )
        
        # Signal handler pour fermeture propre
        def signal_handler(sig, frame):
            self.stdout.write(
                self.style.WARNING('\nArrêt du service MQTT...')
            )
            mqtt_client.disconnect()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Rester en attente
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            mqtt_client.disconnect()
