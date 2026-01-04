from django.apps import AppConfig


class DhtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DHT'
    
    def ready(self):
        """Enregistrer les signaux quand l'app est prête"""
        import DHT.signals  # Import pour enregistrer les signaux
