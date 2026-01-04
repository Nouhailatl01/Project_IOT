#!/usr/bin/env python
"""
Script pour tester la configuration email
Utilisez: python manage.py shell < test_email_config.py
"""

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("TEST DE CONFIGURATION EMAIL")
print("=" * 60)

print("\n📋 Configuration actuelle:")
print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"  ALERT_EMAIL: {getattr(settings, 'ALERT_EMAIL', 'Non configuré')}")

if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER.startswith('your-'):
    print("\n❌ ERREUR: EMAIL_HOST_USER non configuré!")
    print("   Veuillez éditer projet/settings.py et remplacer:")
    print("     EMAIL_HOST_USER = 'your-email@gmail.com'")
    print("   Par votre vrai email.")
    exit(1)

print("\n📧 Tentative d'envoi d'email de test...")

try:
    subject = "🧪 Test Email - Système de Surveillance DHT11"
    message = """
Ceci est un email de test du système de surveillance DHT11.

Si vous recevez cet email, cela signifie que la configuration SMTP fonctionne correctement!

Données de test:
- Incident ID: TEST-001
- Niveau: 1/7
- Température: 25.5°C
- Humidité: 65%

Cordialement,
Système de Surveillance
"""
    
    alert_email = getattr(settings, 'ALERT_EMAIL', 'nouhaila.touil.23@ump.ac.ma')
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[alert_email],
        fail_silently=False,
    )
    
    print(f"✅ Email envoyé avec succès à {alert_email}!")
    print("\n✨ Configuration SMTP fonctionne correctement!")
    
except Exception as e:
    print(f"\n❌ ERREUR: {str(e)}")
    print(f"   Type: {type(e).__name__}")
    print("\nConsulter EMAIL_CONFIG.txt pour l'aide à la configuration.")
    exit(1)
