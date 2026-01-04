# 📧 Configuration des Emails d'Alerte Incidents

## Vue d'ensemble

Le système envoie automatiquement un email d'alerte à chaque fois qu'un incident est détecté ou escaladé. 

**Email destinataire:** nouhaila.touil.23@ump.ac.ma

---

## ⚙️ Configuration (IMPORTANT!)

### Étape 1: Obtenir les identifiants SMTP

Vous avez besoin d'un compte email avec accès SMTP. Nous recommandons **Gmail** car c'est simple et gratuit.

#### Pour Gmail:

1. Allez sur https://myaccount.google.com
2. Cliquez sur "Sécurité" en haut à droite
3. Activez l'authentification **2FA** (deux facteurs)
4. Allez à **"Mots de passe d'application"**
5. Sélectionnez:
   - Application: **Mail**
   - Appareil: **Windows** (ou autre)
6. Cliquez sur "Générer"
7. Copiez le mot de passe généré (sans espaces)

### Étape 2: Configurer Django

Ouvrez `projet/settings.py` et cherchez cette section:

```python
# ===== CONFIGURATION EMAIL =====
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'          # ← À REMPLACER
EMAIL_HOST_PASSWORD = 'your-app-password'        # ← À REMPLACER
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'      # ← À REMPLACER

ALERT_EMAIL = 'nouhaila.touil.23@ump.ac.ma'      # Email d'alerte
```

**Remplacez:**
- `'your-email@gmail.com'` → Votre adresse Gmail (ex: `mon.email@gmail.com`)
- `'your-app-password'` → Le mot de passe d'application copié à l'étape 1

### Étape 3: Tester la configuration

```bash
python manage.py shell < test_email_config.py
```

Vous devriez voir:
```
✅ Email envoyé avec succès à nouhaila.touil.23@ump.ac.ma!
✨ Configuration SMTP fonctionne correctement!
```

---

## 🔧 Autres fournisseurs SMTP

### Outlook/Hotmail:
```python
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@outlook.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe'
```

### Sendgrid:
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'votre-clé-api-sendgrid'
```

### Autre SMTP personnalisé:
Consultez la documentation de votre fournisseur email.

---

## 📬 Quand les emails sont envoyés?

Les emails d'alerte sont envoyés automatiquement dans les cas suivants:

### 1. **Création d'un nouvel incident**
   - Quand la température sort des limites (< 2°C ou > 8°C)
   - Email contenant:
     - ID de l'incident
     - Niveau d'escalade (1/7)
     - Opérateurs alertés
     - Données actuelles du capteur

### 2. **Escalade d'incident**
   - Quand personne ne répond et la température reste anormale
   - Le niveau augmente de 1 jusqu'à 7
   - Un email est envoyé à chaque nouvelle escalade
   - Nouveau personnel alerté selon le niveau

### 3. **Contenu de l'email**

```
Sujet: 🚨 ALERTE INCIDENT #42 - Niveau 1

📊 DÉTAILS DE L'INCIDENT:
- ID Incident: #42
- Niveau d'escalade: 1/7
- Statut: Ouvert
- Date/Heure: 04/01/2025 14:30:45

👥 OPÉRATEURS À ALERTER:
- Opérateur 1

🌡️ DONNÉES CAPTEUR:
- Température max: 9.2°C
- Température min: 9.2°C
- Humidité max: 65%
- Humidité min: 65%

⚠️ ACTION REQUISE:
Veuillez vous connecter au tableau de bord pour vérifier cet incident 
et prendre les mesures appropriées.
```

---

## 🐛 Dépannage

### Erreur: "Email SMTP non configuré"

**Cause:** `EMAIL_HOST_USER` n'est pas configuré

**Solution:**
1. Ouvrez `projet/settings.py`
2. Cherchez `EMAIL_HOST_USER = 'your-email@gmail.com'`
3. Remplacez par votre vrai email

### Erreur: "SMTPAuthenticationError"

**Cause:** Mauvais mot de passe ou authentification échouée

**Solution:**
1. Vérifiez le mot de passe d'application (pas votre mot de passe Gmail!)
2. Assurez-vous que l'authentification 2FA est activée
3. Vérifiez que vous avez généré le bon mot de passe d'application (Mail + votre OS)

### Erreur: "SMTPServerDisconnected"

**Cause:** Problème de connexion au serveur SMTP

**Solution:**
1. Vérifiez votre connexion Internet
2. Vérifiez que `EMAIL_HOST`, `EMAIL_PORT` et `EMAIL_USE_TLS` sont corrects
3. Pour Gmail: Assurez-vous que "Accès aux applications moins sécurisées" est autorisé

### Les emails ne sont pas envoyés en production

**Cause:** Le serveur n'a pas accès à Internet ou au serveur SMTP

**Solution:**
1. Vérifiez la connexion Internet du serveur
2. Vérifiez les logs Django pour les erreurs
3. Testez avec: `python manage.py shell < test_email_config.py`

---

## 📊 Logging des emails

Les tentatives d'envoi d'email sont enregistrées dans la console Django:

```
   ✉️  Email d'alerte envoyé à nouhaila.touil.23@ump.ac.ma
```

Ou en cas d'erreur:

```
   ⚠️  ERREUR lors de l'envoi d'email: [SMTPAuthenticationError]
       Type d'erreur: SMTPAuthenticationError
```

L'incident est créé même si l'email échoue. Vous pouvez toujours voir l'incident dans le tableau de bord.

---

## 🔐 Sécurité

- ✅ Utilisez toujours **TLS** pour les connexions SMTP
- ✅ Utilisez des **mots de passe d'application** au lieu de vrais mots de passe
- ✅ Ne partagez jamais `EMAIL_HOST_PASSWORD` en public
- ✅ Pour les serveurs de production, utilisez des variables d'environnement

### Exemple avec variables d'environnement:

```python
import os

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

---

## ✨ C'est tout!

Vos alertes par email sont maintenant configurées. Testez en déclenchant manuellement un incident avec une température hors limites!

Pour toute question, consultez `EMAIL_CONFIG.txt`
