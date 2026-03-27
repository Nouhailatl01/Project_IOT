#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
sys.path.insert(0, r'c:\Users\nouha\Desktop\pythonProject - Copi')
django.setup()

# Test email
from django.core.mail import send_mail
from django.conf import settings

print("\n" + "="*60)
print("TEST DE CONFIGURATION EMAIL")
print("="*60)

print("\n📋 Configuration actuelle:")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"  ALERT_EMAIL: {getattr(settings, 'ALERT_EMAIL', 'Non configuré')}")

print("\n📧 Tentative d'envoi d'email de test...")

try:
    send_mail(
        subject="🧪 Test Email - Système DHT11",
        message="Ceci est un test de configuration SMTP. Si vous recevez cet email, c'est que tout fonctionne!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[getattr(settings, 'ALERT_EMAIL', 'nouhaila.touil.23@ump.ac.ma')],
        fail_silently=False,
    )
    
    print("\n✅ Email envoyé avec succès!")
    print("Vérifiez votre boîte: nouhaila.touil.23@ump.ac.ma")
    
except Exception as e:
    print(f"\n❌ ERREUR: {str(e)}")
    print(f"Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
