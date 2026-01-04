## 📊 SYSTÈME DE GESTION DES INCIDENTS - RÉCAPITULATIF

### 🎯 Vue d'ensemble
Un système complet de détection d'incidents basé sur la température avec escalade opérateurs et archive.

---

## 🌡️ RÈGLES D'INCIDENT

### Condition de détection
- **Température normale** : Entre 2°C et 8°C inclus ✓
- **Incident** : Température < 2°C OU Température > 8°C ⚠️

### Logique
1. À chaque nouvelle mesure hors plage → **Compteur +1**
2. Quand la température revient à la normale → **Incident fermé**
3. Compteur revient à **0**

---

## 👥 ESCALADE OPÉRATEURS

### Affichage conditionnel
- **Compteur ≥ 1** → Opérateur 1 s'affiche
- **Compteur ≥ 4** → Opérateur 2 s'affiche
- **Compteur ≥ 7** → Opérateur 3 s'affiche

### Actions pour chaque opérateur
✓ Case "Accusé de réception" (checkbox)
✓ Champ "Commentaire" (textarea)
✓ Bouton "Valider"
✓ Affichage de la dernière validation avec timestamp

---

## 🔌 URLs & ENDPOINTS

### Pages Publiques
- `/` → Dashboard public (mesures en temps réel)
- `/graph_temp/` → Graphe température
- `/graph_hum/` → Graphe humidité
- `/incident/archive/` → Archive des incidents fermés

### Pages Opérateurs (login required)
- `/login/` → Écran de connexion
- `/logout/` → Déconnexion
- `/dashboard/` → Dashboard opérateur (avec incidents et API tester)
- `/incident/<id>/` → Détails d'un incident archivé

### APIs JSON
- `GET /api/` → Liste tous les enregistrements DHT
- `POST /api/post` → Envoyer une nouvelle mesure (temp, hum)
- `GET /latest/` → Dernière mesure (JSON)
- `GET /incident/status/` → État de l'incident actuel
- `POST /incident/update/` → Valider accusé + commentaire d'un opérateur

---

## 📱 STRUCTURE DES DONNÉES

### Modèle Dht11
```
- temp: Float (température en °C)
- hum: Float (humidité en %)
- dt: DateTime (timestamp)
```

### Modèle Incident
```
- start_at: DateTime (début)
- end_at: DateTime (fin, null si ouvert)
- is_open: Boolean (ouvert/fermé)
- counter: Integer (compteur d'alertes)
- max_temp: Float (température maximale enregistrée)

- op1_ack: Boolean
- op1_comment: TextField
- op1_saved_at: DateTime

- op2_ack: Boolean
- op2_comment: TextField
- op2_saved_at: DateTime

- op3_ack: Boolean
- op3_comment: TextField
- op3_saved_at: DateTime
```

### Modèle Operateur
```
- user: OneToOneField(User)
- level: Integer (1, 2 ou 3)
- is_active: Boolean
- created_at: DateTime
```

---

## 🔐 AUTHENTIFICATION

### Comptes de test
| Utilisateur | Mot de passe | Niveau |
|-------------|-------------|--------|
| `op1` | `password` | Opérateur 1 |
| `op2` | `password` | Opérateur 2 |
| `op3` | `password` | Opérateur 3 |

**Creation de nouveaux opérateurs :**
```bash
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
import django
django.setup()

from django.contrib.auth.models import User
from DHT.models import Operateur

user = User.objects.create_user(
    username='op_nouveau',
    password='password123',
    first_name='Nouveau',
    is_staff=False,
    is_active=True
)

Operateur.objects.create(
    user=user,
    level=1,
    is_active=True
)
"
```

---

## 📤 EXEMPLES D'API

### Créer une mesure
```bash
curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{
    "temp": 15.5,
    "hum": 65.0
  }'
```

### Vérifier l'état incident
```bash
curl http://localhost:8000/incident/status/
```

Réponse :
```json
{
  "id": 1,
  "is_open": true,
  "counter": 5,
  "max_temp": 15.5,
  "start_at": "2025-12-31T10:30:00Z",
  "end_at": null,
  "op1_ack": false,
  "op1_comment": "",
  "op1_saved_at": null
}
```

### Valider accusé opérateur
```bash
curl -X POST http://localhost:8000/incident/update/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{
    "op": 1,
    "ack": true,
    "comment": "Problème identifié, je me charge de..."
  }'
```

---

## 🎨 INTERFACES CRÉÉES

### 1. Login (`/login/`)
- Gradient moderne (bleu-violet)
- Authentification sécurisée
- Messages d'erreur clairs

### 2. Dashboard Opérateur (`/dashboard/`)
- **Mesures en temps réel** (température + humidité)
- **État incident** avec badge
- **Panels opérateurs dynamiques** (affichage basé sur compteur)
- **Tester l'API** avec inputs et réponse en direct
- Rafraîchissement auto toutes les 2-3 secondes

### 3. Archive Incidents (`/incident/archive/`)
- Tableau des incidents fermés
- Statistiques globales
- Lien vers détails

### 4. Détails Incident (`/incident/<id>/`)
- Vue complète de l'incident
- Informations opérateurs
- Commentaires affichés

---

## 🚀 UTILISATION

### Démarrer le serveur
```bash
cd "C:\Users\nouha\Desktop\pythonProject - Copi"
python manage.py runserver
```

### Accès
- Dashboard opérateur: `http://localhost:8000/dashboard/`
- Dashboard public: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`

---

## ✅ FONCTIONNALITÉS COMPLÉTÉES

✓ Détection automatique d'incidents (T < 2 ou T > 8)
✓ Compteur d'alertes incrémenté
✓ Escalade opérateurs (1 → 2 → 3)
✓ Accusé de réception avec checkbox
✓ Commentaires persistants en BDD
✓ Valeur d'affichage after refresh
✓ Archive des incidents fermés
✓ Page détails incident
✓ Authentification opérateurs
✓ API tester intégrée
✓ Interface responsive et moderne

---

## 🔄 FLUX D'UN INCIDENT

1. **Mesure reçue avec T < 2 ou T > 8**
   → Incident créé si inexistant
   → Compteur = 1

2. **Nouvelle mesure hors plage**
   → Compteur += 1
   → Opérateurs affichés dynamiquement

3. **Compteur ≥ 4**
   → Opérateur 2 s'affiche

4. **Compteur ≥ 7**
   → Opérateur 3 s'affiche

5. **Opérateurs valident**
   → Accusé + commentaire sauvegardés
   → Timestamp enregistré

6. **T revient entre 2-8°C**
   → Incident fermé (is_open = False)
   → end_at défini
   → Archivé automatiquement

7. **Consultation archive**
   → Tableau des incidents fermés
   → Clic "Détails" pour voir infos complètes

---

## 📝 NOTES

- localStorage utilisé temporairement côté client
- BDD = source de vérité
- Refreshes auto chaque 2-3 sec
- CSRF protection active
- Login requis pour `/dashboard/`
