# 🔧 DOCUMENTATION TECHNIQUE - SYSTÈME D'ESCALADE

## 📐 Architecture

### Modèles Django

#### Incident (modifié)
```python
class Incident(models.Model):
    # Champs de base
    start_at = DateTimeField(auto_now_add=True)
    end_at = DateTimeField(null=True, blank=True)
    is_open = BooleanField(default=True)
    is_archived = BooleanField(default=False)
    
    # Mesures
    counter = IntegerField(default=0)
    max_temp = FloatField(default=0)
    is_product_lost = BooleanField(default=False)
    
    # Escalade
    current_escalation_level = IntegerField(default=1)  # 1, 2 ou 3
    escalation_counter = IntegerField(default=0)  # 0-3
    escalated_to_op2_at = DateTimeField(null=True)
    escalated_to_op3_at = DateTimeField(null=True)
    
    # Réactions opérateurs
    op1_responded = BooleanField(default=False)
    op2_responded = BooleanField(default=False)
    op3_responded = BooleanField(default=False)
    
    op1_responded_at = DateTimeField(null=True)
    op2_responded_at = DateTimeField(null=True)
    op3_responded_at = DateTimeField(null=True)
    
    op1_comment = TextField(blank=True)
    op2_comment = TextField(blank=True)
    op3_comment = TextField(blank=True)
```

---

## 🔌 API REST

### Endpoint: POST `/incident/update/`

#### Request Payload
```json
{
  "op": 1,
  "responded": true,
  "comment": "Capteur remplacé, température normale"
}
```

#### Paramètres
| Param | Type | Description |
|-------|------|-------------|
| `op` | int | Niveau d'opérateur (1, 2, ou 3) |
| `responded` | bool | L'opérateur a-t-il réagi? |
| `comment` | string | Commentaire de l'opérateur |

#### Response
```json
{
  "id": 8,
  "start_at": "2026-01-03T23:00:00Z",
  "end_at": "2026-01-03T23:30:00Z",
  "is_open": false,
  "is_archived": true,
  "counter": 4,
  "max_temp": 11.5,
  "current_escalation_level": 2,
  "escalation_counter": 1,
  "op1_responded": false,
  "op2_responded": true,
  "op2_comment": "...",
  "op2_responded_at": "2026-01-03T23:30:00Z",
  "escalated_to_op2_at": "2026-01-03T23:15:00Z",
  "is_product_lost": false
}
```

---

## 🔄 Logique d'escalade (détails)

### Fluxgramme de l'API

```
POST /incident/update/
│
├─ Récupérer incident ouvert
│
├─ Enregistrer réaction OP1/OP2/OP3
│  ├─ op{n}_responded = responded
│  ├─ op{n}_comment = comment
│  └─ op{n}_responded_at = now()
│
├─ LOGIQUE D'ESCALADE
│  │
│  ├─ Si responded=true ET comment non-vide:
│  │  ├─ escalation_counter = 0  ✅ RÉINITIALISER
│  │  ├─ is_open = False  ✅ FERMER
│  │  ├─ is_archived = True  ✅ ARCHIVER
│  │  └─ end_at = now()
│  │
│  └─ Si responded=false:
│     ├─ Si current_escalation_level = OP actuel:
│     │  └─ Si escalation_counter >= 3:
│     │     ├─ current_escalation_level += 1  ⬆️ ESCALADE
│     │     ├─ escalation_counter = 0
│     │     └─ escalated_to_OP{n}_at = now()
│     └─ Sinon: continuer...
│
└─ Retourner incident mis à jour
```

### Exemple avec détails

**Situation: 3 incidents sans réaction d'OP1**

```
Incident 1:
  - escalation_counter = 1
  - current_escalation_level = 1
  - Sauvegardé

Incident 2:
  - escalation_counter = 2
  - current_escalation_level = 1
  - Sauvegardé

Incident 3:
  - escalation_counter = 3
  - current_escalation_level = 1
  - ⚠️ CONDITION ATTEINTE: counter >= 3
  - ✅ Escalade décidée:
    - current_escalation_level = 2
    - escalation_counter = 0
    - escalated_to_op2_at = maintenant
```

---

## 🎨 Frontend - Dashboard

### Composants clés

#### Affichage du statut incident
```html
<div class="incident-box incident-alert">
  <div class="incident-title">⚠️ INCIDENT EN COURS</div>
  <div class="incident-info">
    Incident: Escalade OP2 (2/3)
  </div>
</div>
```

#### Formulaires opérateurs (dynamiques)
```javascript
function updateOperators(incident) {
  // Afficher les opérateurs en fonction de l'escalade
  const showOp1 = true;  // Toujours
  const showOp2 = incident.escalated_to_op2_at !== null;
  const showOp3 = incident.escalated_to_op3_at !== null;
  
  // Générer les formulaires HTML
}
```

#### Validation stricte du formulaire
```javascript
function validateOp(level) {
  const responded = document.querySelector(`[data-level="${level}"]`).checked;
  const comment = document.querySelector(`.op-comment[data-level="${level}"]`).value;
  
  // ❌ Refuser si pas de commentaire
  if (responded && !comment.trim()) {
    showAlert('Veuillez ajouter un commentaire', 'error');
    return;
  }
  
  // ✅ Envoyer à l'API
  fetch('/incident/update/', {
    method: 'POST',
    body: JSON.stringify({op: level, responded, comment})
  })
}
```

---

## 📦 Migration Django

### 0005_incident_escalation_system.py

```python
class Migration(migrations.Migration):
    dependencies = [
        ('DHT', '0004_incident_is_product_lost_operateur_email_and_more'),
    ]

    operations = [
        # Suppression des champs anciens
        migrations.RemoveField(model_name='incident', name='op1_ack'),
        migrations.RemoveField(model_name='incident', name='op2_ack'),
        migrations.RemoveField(model_name='incident', name='op3_ack'),
        migrations.RemoveField(model_name='incident', name='op1_saved_at'),
        migrations.RemoveField(model_name='incident', name='op2_saved_at'),
        migrations.RemoveField(model_name='incident', name='op3_saved_at'),
        
        # Ajout des nouveaux champs
        migrations.AddField(
            model_name='incident',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        # ... (autres champs)
    ]
```

---

## 🧪 Tests

### test_escalation.py

```python
# Créer un incident
incident = Incident.objects.create(
    is_open=True,
    current_escalation_level=1,
    escalation_counter=1
)

# Simuler réaction OP1
incident.op1_responded = True
incident.op1_comment = "Commentaire"
incident.escalation_counter = 0

# Simuler escalade
incident.escalation_counter = 3
if incident.escalation_counter >= 3:
    incident.current_escalation_level = 2
    incident.escalated_to_op2_at = timezone.now()

# Vérifier fermeture
incident.is_open = False
incident.is_archived = True
```

---

## ⚡ Performance

### Requêtes optimisées
- Incident récupéré avec `.first()` (une seule requête)
- Pas de boucles N+1
- Timestamps en UTC pour cohérence

### Caching possible
```python
# Ajouter du caching si nécessaire
from django.views.decorators.cache import cache_page

@cache_page(5)  # Cache 5 secondes
def incident_status(request):
    incident = Incident.objects.filter(is_open=True).first()
```

---

## 🔐 Sécurité

### CSRF Protection
```javascript
headers: {
  'Content-Type': 'application/json',
  'X-CSRFToken': getCookie('csrftoken')  // ← Important!
}
```

### Validation serveur
```python
try:
    op = int(request.data.get("op"))
    responded = bool(request.data.get("responded"))
    comment = request.data.get("comment", "").strip()
    
    # Valider que l'incident existe et est ouvert
    if not incident or not incident.is_open:
        return Response({"error": "Invalid incident"}, status=400)
```

### Authentification
- Seuls les `Operateur` actifs peuvent accéder
- Vérification du `@login_required`

---

## 📈 Métriques possibles

### À suivre
```python
- Temps moyen de réaction par opérateur
- Nombre d'escalades par jour
- Taux de résolution au niveau OP1
- Incidents archivés avec/sans commentaire
```

### Requête analytics
```python
from django.db.models import Count, Avg
from datetime import timedelta

# Incidents escaladés à OP2
IncidentmBatch = Incident.objects.filter(
    current_escalation_level__gte=2,
    escalated_to_op2_at__isnull=False
).count()

# Temps moyen pour OP1
avg_time = Incident.objects.filter(
    op1_responded=True
).aggregate(
    avg=Avg(F('op1_responded_at') - F('start_at'))
)
```

---

## 🚨 Logs et debugging

### Activer les logs Django
```python
# Dans settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'DHT': {'level': 'DEBUG', 'handlers': ['console']},
    }
}
```

### Voir les requêtes
```bash
python manage.py shell
>>> from DHT.models import Incident
>>> Incident.objects.filter(is_archived=True)
>>> incident.op1_responded, incident.op1_comment
```

---

**Documentation complète pour développeurs**  
**Mise à jour:** 4 janvier 2026
