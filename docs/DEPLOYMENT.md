# 📋 Guide de Déploiement - PythonAnywhere

## Étapes Complètes pour Production

### 1. Créer un compte PythonAnywhere
- Aller sur [pythonanywhere.com](https://www.pythonanywhere.com)
- Créer compte (free ou payant)
- Valider email

### 2. Upload du Code
```bash
cd ~/
git clone <your-repo-url>
cd pythonProject
```

### 3. Configuration Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.8 mysite
pip install -r requirements.txt
```

### 4. Base de Données PostgreSQL
- Panel PythonAnywhere → Databases
- Créer PostgreSQL database
- Noter credentials

### 5. Configuration Django
Modifier `projet/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_username.postgres.pythonanywhere-services.com',
        'PORT': '5432',
    }
}
```

### 6. Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Web App Configuration
- Panel Web → Add new web app
- Domain: votre domaine
- Python: Python 3.8
- Framework: Manual configuration
- Virtualenv: /home/yourusername/.virtualenvs/mysite

### 8. WSGI Configuration
Éditer `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import sys
path = '/home/yourusername/pythonProject'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'projet.settings'
from django.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 9. HTTPS & Certificat
- Panel Web → HTTPS
- Obtenir certificat Let's Encrypt gratuit

### 10. Vérifier
```
https://yourdomain.com
```

---

Voir DOCUMENTATION_TECHNIQUE.md pour plus de détails.
