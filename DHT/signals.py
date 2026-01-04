"""Signaux Django pour gérer les incidents automatiquement avec escalade"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Dht11, Incident
import json

try:
    from .mqtt_client import mqtt_client
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False

MIN_OK = 2
MAX_OK = 8

def send_incident_alert_email(incident):
    """
    Envoyer un email d'alerte quand un incident est créé ou escaladé
    """
    try:
        operators = incident.get_escalation_operators()
        operators_text = ', '.join([f'Opérateur {op}' for op in operators])
        
        subject = f'🚨 ALERTE INCIDENT #{incident.id} - Niveau {incident.escalation_level}'
        
        message = f"""
Bonjour,

Un incident a été détecté et créé dans le système de surveillance des capteurs DHT11.

📊 DÉTAILS DE L'INCIDENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID Incident: #{incident.id}
Niveau d'escalade: {incident.escalation_level}/7
Statut: {incident.get_status_display()}
Date/Heure: {incident.start_at.strftime('%d/%m/%Y %H:%M:%S')}

👥 OPÉRATEURS À ALERTER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{operators_text}

🌡️  DONNÉES CAPTEUR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Température max: {incident.max_temp}°C
Température min: {incident.min_temp}°C
Humidité max: {incident.max_hum}%
Humidité min: {incident.min_hum}%

⚠️  ACTION REQUISE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Veuillez vous connecter au tableau de bord pour vérifier cet incident et prendre les mesures appropriées.

Cet email a été généré automatiquement par le système de surveillance.
Ne répondez pas directement à cet email.

Cordialement,
Système d'Alerte Automatique
"""
        
        # Récupérer l'email configuré (ou utiliser par défaut)
        alert_email = getattr(settings, 'ALERT_EMAIL', 'nouhaila.touil.23@ump.ac.ma')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@system.com')
        
        # Vérifier que les paramètres SMTP sont configurés
        if not hasattr(settings, 'EMAIL_HOST_USER') or not settings.EMAIL_HOST_USER:
            print(f"   ⚠️  Email SMTP non configuré. Alerte non envoyée.")
            print(f"       Veuillez configurer EMAIL_HOST_USER dans settings.py")
            return False
        
        # Envoyer l'email
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[alert_email],
            fail_silently=False,
        )
        
        print(f"   ✉️  Email d'alerte envoyé à {alert_email}")
        return True
    except Exception as e:
        print(f"   ⚠️  ERREUR lors de l'envoi d'email: {str(e)}")
        print(f"       Type d'erreur: {type(e).__name__}")
        # On continue le processus même si l'email échoue
        return False

@receiver(post_save, sender=Dht11)
def handle_dht_reading(sender, instance, created, **kwargs):
    """
    Gérer automatiquement les incidents quand une nouvelle lecture DHT11 est enregistrée.
    
    Logique d'escalade :
    - Incident 1 (escalation_level=1): Alerter OP1
    - Incident 2 (escalation_level=2): Alerter OP1
    - Incident 3 (escalation_level=3): Alerter OP1
    - Incident 4 (escalation_level=4): Alerter OP1 + OP2
    - Incident 5 (escalation_level=5): Alerter OP1 + OP2
    - Incident 6 (escalation_level=6): Alerter OP1 + OP2
    - Incident 7 (escalation_level=7): Alerter OP1 + OP2 + OP3
    - Incident 8+ (escalation_level=8+): Alerter OP1 + OP2 + OP3
    
    - Si quelqu'un réagit (responded=True + commentaire) → Incident archivé immédiatement
    - Si aucun réagit → escalation_level augmente jusqu'à 7 (escalade maximale)
    """
    if not created:
        return  # Ne traiter que les nouvelles lectures
    
    t = instance.temp
    h = instance.hum
    
    # Si pas de température, ignorer
    if t is None:
        print(f"⚠️ Signal: Température None ignorée")
        return
    
    print(f"\n🔔 Signal post_save Dht11(#{instance.id}): temp={t}°C, hum={h}%")
    
    # Vérifier si température est hors limites
    is_incident = (t < MIN_OK or t > MAX_OK)
    print(f"   → Anomalie détectée: {is_incident} (min={MIN_OK}, max={MAX_OK})")
    
    # Récupérer l'incident ouvert (s'il existe)
    incident = Incident.objects.filter(is_open=True, status='open').order_by("-start_at").first()
    
    if is_incident:
        # Anomalie détectée
        if incident is None:
            # Créer un nouvel incident avec escalation_level=1
            incident = Incident.objects.create(
                is_open=True,
                status='open',
                escalation_level=1,
                max_temp=t,
                min_temp=t,
                max_hum=h,
                min_hum=h,
                start_at=timezone.now(),
                escalation_history=json.dumps({
                    "1": {
                        "timestamp": timezone.now().isoformat(),
                        "temp": t,
                        "hum": h,
                        "operators": [1],
                        "message": "Incident 1 détecté - Alerter Op1"
                    }
                })
            )
            print(f"   ✅ NOUVEL INCIDENT créé:")
            print(f"      ID={incident.id}, escalation_level={incident.escalation_level}")
            print(f"      Opérateurs à alerter: {incident.get_escalation_operators()}")
            
            # 📧 ENVOYER EMAIL D'ALERTE
            send_incident_alert_email(incident)
        else:
            # Un incident est ouvert - vérifier s'il faut escalader
            if not incident.is_resolved():
                # Personne n'a réagi encore - escalader jusqu'à 7 max
                if incident.escalation_level < 7:
                    incident.escalation_level += 1
                    print(f"   📈 ESCALADE incident #{incident.id}:")
                    print(f"      Niveau: {incident.escalation_level}")
                    print(f"      Opérateurs à alerter: {incident.get_escalation_operators()}")
                    
                    # Ajouter à l'historique d'escalade
                    try:
                        history = json.loads(incident.escalation_history) if incident.escalation_history else {}
                    except:
                        history = {}
                    
                    history[str(incident.escalation_level)] = {
                        "timestamp": timezone.now().isoformat(),
                        "temp": t,
                        "hum": h,
                        "operators": incident.get_escalation_operators(),
                        "message": f"Incident {incident.escalation_level} - Alerter {', '.join([f'Op{op}' for op in incident.get_escalation_operators()])}"
                    }
                    incident.escalation_history = json.dumps(history)
                    
                    # Sauvegarder avant d'envoyer l'email
                    incident.save()
                    
                    # 📧 ENVOYER EMAIL D'ALERTE POUR L'ESCALADE
                    send_incident_alert_email(incident)
                    return  # Important: sortir après escalade
                else:
                    print(f"   ⚠️ Escalade maximale atteinte (niveau {incident.escalation_level})")
            else:
                print(f"   ℹ️ Incident #{incident.id} déjà résolu par un opérateur")
            
            # Mettre à jour les extrêmes de température/humidité
            if t > incident.max_temp:
                incident.max_temp = t
            if t < incident.min_temp:
                incident.min_temp = t
            if h > incident.max_hum:
                incident.max_hum = h
            if h < incident.min_hum:
                incident.min_hum = h
                
            incident.save()
    else:
        # Température OK
        if incident is not None and incident.is_open:
            incident.is_open = False
            incident.status = 'archived'
            incident.end_at = timezone.now()
            incident.save()
            print(f"   ✅ INCIDENT FERMÉ ET ARCHIVÉ:")
            print(f"      ID={incident.id}, durée={(incident.end_at - incident.start_at)}")
            print(f"      Temp: min={incident.min_temp}°C, max={incident.max_temp}°C")
            print(f"      Hum: min={incident.min_hum}%, max={incident.max_hum}%")
            
            # Publier l'incident résolu via MQTT
            if MQTT_AVAILABLE and mqtt_client.connected:
                mqtt_client.publish_incident(incident)
        else:
            print(f"   ℹ️ Température OK, aucun incident ouvert")


@receiver(post_save, sender=Incident)
def incident_saved(sender, instance, created, **kwargs):
    """
    Signal appelé quand un incident est créé ou modifié
    Publie l'incident via MQTT si le client est connecté
    """
    if MQTT_AVAILABLE and created and mqtt_client.connected:
        # Incident nouvellement créé
        mqtt_client.publish_incident_alert(instance)
        print(f"📡 Incident #{instance.id} publié via MQTT")
