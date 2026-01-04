#!/usr/bin/env python
"""
Script interactif de configuration email
Exécutez: python configure_email.py
"""

import os
import sys

def get_input(prompt, default=None):
    """Récupérer l'entrée de l'utilisateur"""
    if default:
        prompt += f" [{default}]: "
    else:
        prompt += ": "
    
    value = input(prompt).strip()
    return value if value else default

def main():
    print("\n" + "="*60)
    print("🔧 CONFIGURATION EMAIL - SYSTÈME DE SURVEILLANCE DHT11")
    print("="*60)
    
    print("\n📧 Quel fournisseur email utilisez-vous?")
    print("  1. Gmail (recommandé)")
    print("  2. Outlook/Hotmail")
    print("  3. Autre SMTP")
    
    provider = get_input("\nChoisissez (1-3)", "1")
    
    config = {}
    
    if provider == "1":  # Gmail
        config['EMAIL_HOST'] = 'smtp.gmail.com'
        config['EMAIL_PORT'] = 587
        config['EMAIL_USE_TLS'] = True
        email = get_input("Votre adresse Gmail")
        if not email.endswith('@gmail.com'):
            print("⚠️  Attention: Votre email ne se termine pas par @gmail.com")
        config['EMAIL_HOST_USER'] = email
        password = get_input("Mot de passe d'application Gmail")
        config['EMAIL_HOST_PASSWORD'] = password
        
    elif provider == "2":  # Outlook
        config['EMAIL_HOST'] = 'smtp.office365.com'
        config['EMAIL_PORT'] = 587
        config['EMAIL_USE_TLS'] = True
        config['EMAIL_HOST_USER'] = get_input("Votre adresse Outlook")
        config['EMAIL_HOST_PASSWORD'] = get_input("Votre mot de passe")
        
    else:  # Autre
        config['EMAIL_HOST'] = get_input("SMTP Host")
        config['EMAIL_PORT'] = int(get_input("SMTP Port", "587"))
        config['EMAIL_USE_TLS'] = get_input("Utiliser TLS? (y/n)", "y").lower() == 'y'
        config['EMAIL_HOST_USER'] = get_input("Email/Utilisateur")
        config['EMAIL_HOST_PASSWORD'] = get_input("Mot de passe")
    
    config['DEFAULT_FROM_EMAIL'] = get_input("Email expéditeur (from)", config['EMAIL_HOST_USER'])
    config['ALERT_EMAIL'] = get_input("Email destinataire des alertes", "nouhaila.touil.23@ump.ac.ma")
    
    # Générer le code à ajouter
    print("\n" + "="*60)
    print("📝 CODE À AJOUTER DANS projet/settings.py:")
    print("="*60 + "\n")
    
    code = f"""
# ===== CONFIGURATION EMAIL =====
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '{config['EMAIL_HOST']}'
EMAIL_PORT = {config['EMAIL_PORT']}
EMAIL_USE_TLS = {str(config['EMAIL_USE_TLS']).lower()}
EMAIL_HOST_USER = '{config['EMAIL_HOST_USER']}'
EMAIL_HOST_PASSWORD = '{config['EMAIL_HOST_PASSWORD']}'
DEFAULT_FROM_EMAIL = '{config['DEFAULT_FROM_EMAIL']}'

# Email destinataire pour les alertes incidents
ALERT_EMAIL = '{config['ALERT_EMAIL']}'
"""
    
    print(code)
    
    print("\n" + "="*60)
    print("✅ ÉTAPES SUIVANTES:")
    print("="*60)
    print("\n1. Ouvrez le fichier: projet/settings.py")
    print("2. Cherchez ou créez la section '# ===== CONFIGURATION EMAIL ====='")
    print("3. Remplacez-la par le code ci-dessus")
    print("4. Sauvegardez le fichier")
    print("5. Testez la configuration avec: python manage.py shell < test_email_config.py")
    
    print("\n💾 Voulez-vous que je sauvegarde cette configuration dans un fichier?")
    save = get_input("(y/n)", "y")
    
    if save.lower() == 'y':
        with open('email_config_output.txt', 'w') as f:
            f.write(code)
        print("\n✅ Configuration sauvegardée dans: email_config_output.txt")
    
    print("\n🎉 Configuration complétée!")
    print("Pour plus d'infos: voir EMAIL_SETUP_GUIDE.md\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnnulation.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
