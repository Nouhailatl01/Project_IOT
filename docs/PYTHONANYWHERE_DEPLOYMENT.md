# Déploiement sur PythonAnywhere - Guide Complet

## Étapes à suivre :

### 1. Préparer votre dépôt GitHub
```bash
cd votre_projet
git add .
git commit -m "Prêt pour PythonAnywhere"
git push origin main
```

### 2. Créer un compte PythonAnywhere
- Allez sur https://www.pythonanywhere.com/
- Créez un compte gratuit ou premium
- Connectez-vous

### 3. Cloner le projet depuis GitHub
Dans la console **Bash** de PythonAnywhere :

```bash
cd /home/votreusername/
git clone https://github.com/votreusername/votreprojet.git
cd votreprojet
```

### 4. Créer un environnement virtuel
```bash
mkvirtualenv --python=/usr/bin/python3.10 monvenv
```

### 5. Installer les dépendances
```bash
pip install -r requirements.txt
pip install gunicorn
pip install whitenoise  # Pour les fichiers statiques
```

### 6. Collecte des fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### 7. Configurer Django Settings
Modifiez `projet/settings.py` pour PythonAnywhere :

```python
# Ajouter PythonAnywhere à ALLOWED_HOSTS
ALLOWED_HOSTS = ['votreusername.pythonanywhere.com', 'localhost', '127.0.0.1']

# Activer CSRF
CSRF_TRUSTED_ORIGINS = ['https://votreusername.pythonanywhere.com']

# Mode production
DEBUG = False
```

### 8. Configurer l'application web dans PythonAnywhere
1. Allez dans l'onglet **Web** → **Add a new web app**
2. Choisissez **Manual Configuration**
3. Choisissez **Python 3.10**
4. Dans **WSGI configuration file**, modifiez le fichier généré :

```python
# /home/votreusername/votreprojet/wsgi.py
import os
import sys
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

path = '/home/votreusername/votreprojet'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'projet.settings'

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
```

### 9. Configurer les variables d'environnement
1. Allez dans **Web** → **Environment variables**
2. Ajouter les variables nécessaires :
   - `DJANGO_SETTINGS_MODULE=projet.settings`
   - Autres clés secrètes

### 10. Migrer la base de données
Dans la console Bash :
```bash
python manage.py migrate
python manage.py createsuperuser  # Créer un admin
```

### 11. Redémarrer l'application web
Dans l'onglet **Web**, cliquez sur le bouton **Reload**

## Troubleshooting

**Erreur 502 Bad Gateway :**
- Vérifier les logs : `/var/log/votreusername.pythonanywhere.com.error.log`
- Vérifier que le virtualenv est bien configuré

**Fichiers statiques ne s'affichent pas :**
```bash
python manage.py collectstatic --noinput --clear
```

**Base de données non trouvée :**
- Les bases SQLite ne sont pas recommandées en production
- Utilisez MySQL : https://help.pythonanywhere.com/pages/UsingMySQL/

## Notes Importantes

1. **SQLite vs MySQL** : Pour production, préférez MySQL (gratuit sur PythonAnywhere)
2. **Secrets** : Ne commitez jamais vos secrets.txt sur GitHub
3. **Logs** : Consultez régulièrement les logs d'erreur PythonAnywhere
4. **SSL** : PythonAnywhere offre HTTPS gratuit via Let's Encrypt
