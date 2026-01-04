# 🎯 CONFIGURATION COMPLÈTE

## 📁 Structure du Projet (Mise à jour)

```
pythonProject - Copi/
│
├── CORE FILES
│   ├── db.sqlite3
│   ├── manage.py
│   └── venv/
│
├── CONFIGURATION
│   └── projet/
│       ├── settings.py ✏️ [APPS: DHT, rest_framework]
│       ├── urls.py
│       ├── asgi.py
│       └── wsgi.py
│
├── APPLICATION (DHT)
│   ├── models.py ✏️
│   │   ├── Operateur (NEW)
│   │   ├── Dht11
│   │   └── Incident
│   │
│   ├── views.py ✏️
│   │   ├── login_view(request)
│   │   ├── logout_view(request)
│   │   ├── dashboard_operator(request)
│   │   └── [others]
│   │
│   ├── api.py ✏️
│   │   └── Dhtviews.perform_create() [LOGIQUE CORRIGÉE]
│   │
│   ├── urls.py ✏️ [+3 routes]
│   │   ├── login/
│   │   ├── logout/
│   │   └── dashboard/
│   │
│   ├── serializers.py
│   ├── admin.py
│   ├── apps.py
│   └── migrations/
│       └── 0003_operateur.py (NEW)
│
├── TEMPLATES (4 fichiers)
│   ├── login.html (NEW)
│   ├── dashboard_operator.html (NEW)
│   ├── incident_archive.html ✏️
│   ├── incident_detail.html ✏️
│   └── [others - public dashboard]
│
├── STATIC
│   └── js/
│       ├── dashboard.js
│       ├── graph_temp.js
│       └── graph_hum.js
│
└── DOCUMENTATION (4 fichiers)
    ├── README.md (existant)
    ├── INCIDENTS_SYSTEM.md (NEW)
    ├── TEST_GUIDE.md (NEW)
    └── CHANGES_SUMMARY.md (NEW)

└── SCRIPTS (2 fichiers)
    ├── create_operators.py (NEW)
    └── test_incidents.py (NEW)
```

---

## 🔧 Configuration Django

### settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DHT',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projet.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard_operator'
```

---

## 🗂️ Routes Principales

### Authentication Routes
```
GET  /login/                              → Écran connexion
POST /login/                              → Traiter connexion
GET  /logout/                             → Déconnexion
GET  /dashboard/                          → Dashboard opérateur [PRIVATE]
```

### Public Routes
```
GET  /                                    → Dashboard public
GET  /graph_temp/                         → Graphe température
GET  /graph_hum/                          → Graphe humidité
GET  /incident/archive/                   → Archive incidents fermés
GET  /incident/<id>/                      → Détails incident
```

### API Routes
```
GET  /api/                                → DList (tous)
POST /api/post                            → Dhtviews (créer)
GET  /latest/                             → Dernière mesure
GET  /incident/status/                    → État incident actuel
POST /incident/update/                    → Valider opérateur
```

---

## 👥 Modèles de Données

### 1. Operateur
```
Field          | Type         | Notes
---|---|---
id             | INT          | Primary Key
user           | FK(User)     | OneToOne, on_delete=CASCADE
level          | INT          | Choices: 1, 2, 3
is_active      | BOOLEAN      | default=True
created_at     | DATETIME     | auto_now_add=True
```

### 2. Dht11
```
Field          | Type         | Notes
---|---|---
id             | INT          | Primary Key
temp           | FLOAT        | nullable, blank
hum            | FLOAT        | nullable, blank
dt             | DATETIME     | auto_now_add=True
```

### 3. Incident
```
Field          | Type         | Notes
---|---|---
id             | INT          | Primary Key
start_at       | DATETIME     | auto_now_add=True
end_at         | DATETIME     | null, blank
is_open        | BOOLEAN      | default=True
counter        | INT          | default=0
max_temp       | FLOAT        | default=0
op1_ack        | BOOLEAN      | default=False
op1_comment    | TEXT         | blank
op1_saved_at   | DATETIME     | null, blank
op2_ack        | BOOLEAN      | default=False
op2_comment    | TEXT         | blank
op2_saved_at   | DATETIME     | null, blank
op3_ack        | BOOLEAN      | default=False
op3_comment    | TEXT         | blank
op3_saved_at   | DATETIME     | null, blank
```

---

## 🔐 Authentification Django

### Users/Permissions
```python
User
├── username: "op1", "op2", "op3"
├── password: "password" (hashed)
├── is_staff: False
├── is_active: True
└── operateur (OneToOne)
```

### Décorateurs utilisés
```python
@login_required(login_url='login')
def dashboard_operator(request):
    if not hasattr(request.user, 'operateur'):
        return redirect('login')
    # ...
```

---

## 📤 API Requests/Responses

### POST /api/post (Créer mesure)
```
REQUEST:
POST /api/post HTTP/1.1
Content-Type: application/json
X-CSRFToken: {token}

{
  "temp": 15.5,
  "hum": 65.0
}

RESPONSE (200):
{
  "id": 42,
  "temp": 15.5,
  "hum": 65.0,
  "dt": "2025-12-31T14:52:30.123456Z"
}
```

### GET /incident/status/
```
RESPONSE (200):
{
  "id": 5,
  "is_open": true,
  "counter": 4,
  "max_temp": 20.5,
  "start_at": "2025-12-31T14:45:00Z",
  "end_at": null,
  "op1_ack": true,
  "op1_comment": "Problème détecté",
  "op1_saved_at": "2025-12-31T14:46:00Z",
  "op2_ack": false,
  "op2_comment": "",
  "op2_saved_at": null,
  "op3_ack": false,
  "op3_comment": "",
  "op3_saved_at": null
}

ou

RESPONSE (200 - pas d'incident):
{
  "is_open": false,
  "counter": 0
}
```

### POST /incident/update/ (Valider opérateur)
```
REQUEST:
POST /incident/update/ HTTP/1.1
Content-Type: application/json
X-CSRFToken: {token}

{
  "op": 1,
  "ack": true,
  "comment": "Situation contrôlée"
}

RESPONSE (200):
{
  "id": 5,
  "is_open": true,
  "counter": 4,
  "max_temp": 20.5,
  ...
  "op1_ack": true,
  "op1_comment": "Situation contrôlée",
  "op1_saved_at": "2025-12-31T14:52:00Z",
  ...
}

ou

ERROR (400):
{
  "error": "no open incident"
}
```

---

## 🧪 Variables de Configuration

### api.py
```python
MIN_OK = 2      # Température minimale OK
MAX_OK = 8      # Température maximale OK

# Incident si T < MIN_OK ou T > MAX_OK
is_incident = (t < MIN_OK or t > MAX_OK)
```

### dashboard_operator.html
```javascript
const MIN_OK = 2;
const MAX_OK = 8;
const KEY_STATE = "dht_incident_state_op_v1";
```

---

## 🎨 Templates

### login.html
- Formulaire connexion
- Gradient (bleu-violet)
- Validation erreurs
- Responsive design

### dashboard_operator.html
- Header avec déconnexion
- Mesures temps réel
- État incident badge
- Panels opérateurs dynamiques
- API tester intégrée
- Rafraîchissement auto (2-3s)

### incident_archive.html
- Tableau incidents fermés
- Statistiques globales
- Durée calculée en JS
- Lien détails
- Design responsive

### incident_detail.html
- Infos complètes incident
- Stat cards (statut, compteur, temp, durée)
- Panels opérateurs avec commentaires
- Affichage accusé (oui/non)
- Timestamps validations

---

## ⚙️ Paramètres Importants

### Escalade Opérateurs
```python
if incident.counter >= 1:  # Op1
    show_op1_panel()

if incident.counter >= 4:  # Op2
    show_op2_panel()

if incident.counter >= 7:  # Op3
    show_op3_panel()
```

### Logique Incident
```python
# Détection
is_incident = (t < 2 or t > 8)

if is_incident:
    if not incident_open:
        create_incident()
    incident.counter += 1
else:
    if incident_open:
        close_incident()
        reset_counter()
```

---

## 🚀 Déploiement

### En production
```bash
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # ou MySQL
        'NAME': 'dbname',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📊 Checklist de Vérification

- [x] Migrations appliquées
- [x] Opérateurs créés (op1, op2, op3)
- [x] Serveur démarre sans erreurs
- [x] Login fonctionne
- [x] Dashboard opérateur accessible
- [x] API POST fonctionne
- [x] Incidents créés correctement
- [x] Opérateurs s'affichent dynamiquement
- [x] Validations sauvegardées
- [x] Archive fonctionne
- [x] Détails affiche infos correctes

**Statut:** ✅ PRODUCTION READY
