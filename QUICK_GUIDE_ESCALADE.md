# 🚀 GUIDE RAPIDE - SYSTÈME D'ESCALADE

## 📌 Vue Rapide

Le système escalade automatiquement les incidents:

```
Anomalie détectée → Incident créé (level=1)
                 ↓
                 Alerter Op1
                 ↓
        Si personne ne réagit → Escalader à level=2
        Si quelqu'un réagit → ARCHIVER IMMÉDIATEMENT
```

---

## 🎯 Les 3 Scénarios Clés

### 1️⃣ Escalade Sans Réaction

```
Level 1 → Op1 alerté
Level 2 → Op1 alerté (continue)
Level 3 → Op1 alerté (continue)
Level 4 → Op1 + Op2 alertés ⭐ (escalade)
Level 5 → Op1 + Op2 alertés
Level 6 → Op1 + Op2 alertés
Level 7 → Op1 + Op2 + Op3 alertés ⭐ (escalade max)
```

**Point clé:** À chaque niveau, de nouveaux opérateurs sont potentiellement alertés.

### 2️⃣ Réaction d'Opérateur

```
Incident(level=5, Op1+Op2 alertés)
        ↓
Op1 clique: "J'ai vu" + écrit commentaire
        ↓
✅ INCIDENT ARCHIVÉ IMMÉDIATEMENT
   - status = "resolved"
   - escalation_level = 0
   - Tous les détails sauvegardés
```

**Point clé:** Dès qu'un opérateur répond, l'incident est archivé.

### 3️⃣ Température Redevient OK

```
Incident(level=3, ouvert)
        ↓
[Lecture: temp=5°C (entre 2 et 8)]
        ↓
✅ INCIDENT FERMÉ AUTOMATIQUEMENT
   - status = "archived"
   - Tous les détails sauvegardés
```

**Point clé:** Si la température redevient normale, l'incident se ferme tout seul.

---

## 🔌 API Endpoints

### Voir l'état courant
```bash
curl http://localhost:8000/incident/status/
```

**Réponse:**
```json
{
  "id": 5,
  "escalation_level": 3,
  "escalation_operators": [1],
  "status": "open",
  "is_open": true
}
```

### Opérateur répond
```bash
curl -X POST http://localhost:8000/incident/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "op": 1,
    "responded": true,
    "comment": "Problème signalé au maintenance"
  }'
```

**Réponse:**
```json
{
  "id": 5,
  "status": "resolved",
  "escalation_level": 0,
  "op1_responded": true,
  "op1_comment": "Problème signalé au maintenance",
  "op1_responded_at": "2026-01-04T14:35:00Z"
}
```

### Lister les incidents archivés
```bash
curl http://localhost:8000/incident/archive/list/
```

### Détails complets d'un incident
```bash
curl http://localhost:8000/incident/archive/5/
```

---

## 💾 Ce Qui Est Sauvegardé

Pour chaque incident archivé:

```
✅ Données des capteurs
   - min/max température
   - min/max humidité

✅ Historique d'escalade complet
   - Chaque niveau avec timestamp
   - Opérateurs alertés
   - État des capteurs

✅ Réactions opérateurs
   - Qui a réagi
   - Quand
   - Leurs commentaires

✅ Métadonnées
   - Durée
   - Statut final
   - Produit perdu (si 10h+ sans réaction)
```

---

## 🧪 Tester Localement

```bash
# Créer un incident de test
python manage.py shell
```

```python
from DHT.models import Dht11, Incident

# Créer une anomalie
Dht11.objects.create(temp=10, hum=50)  # Level 1, Op1 alerté

# Simuler plusieurs anomalies
for i in range(6):
    Dht11.objects.create(temp=11+i, hum=50)

# Vérifier
incident = Incident.objects.filter(is_open=True).first()
print(f"Level: {incident.escalation_level}")  # 7
print(f"Opérateurs: {incident.get_escalation_operators()}")  # [1, 2, 3]

# Simuler réaction
incident.op1_responded = True
incident.op1_comment = "Résolu"
incident.status = "resolved"
incident.escalation_level = 0
incident.save()

print(f"Status: {incident.status}")  # "resolved"
```

---

## 🎛️ Configuration (si besoin)

**Fichier:** `DHT/signals.py`

```python
MIN_OK = 2    # Température minimale acceptable
MAX_OK = 8    # Température maximale acceptable
```

---

## ❓ Troubleshooting

### Le compteur ne remonte pas après une réaction?
→ Vérifiez que l'opérateur a écrit un commentaire (non vide)

### L'incident ne se ferme pas quand temp OK?
→ Vérifiez que la temp est bien entre MIN_OK (2) et MAX_OK (8)

### L'historique est vide?
→ Vérifiez que `escalation_history` est bien une JSONField

---

## 📊 Exemple Complet

```
Temps   Temp  Événement
────────────────────────────────────────
T0:00   9.5°C Incident créé (level=1)
                Alerte: Op1

T0:10   10.2°C Escalade (level=2)
                Alerte: Op1

T0:20   11.0°C Escalade (level=3)
                Alerte: Op1

T0:30   11.5°C Escalade (level=4) ⭐
                Alerte: Op1, Op2

T0:40   12.0°C Escalade (level=5)
                Alerte: Op1, Op2

T0:50   12.5°C Escalade (level=6)
                Alerte: Op1, Op2

T1:00   13.0°C Escalade (level=7) ⭐
                Alerte: Op1, Op2, Op3

T1:35   Op1 répond + commentaire
        ✅ INCIDENT ARCHIVÉ (status=resolved)
           escalation_level = 0
           Tous les détails conservés
```

---

## 🎓 Points Importants à Retenir

1. **Compteur = Niveau d'Escalade** (0-7+)
2. **Opérateurs changent au niveau 4 et 7**
3. **Réaction immédiate = Archivage immédiat**
4. **Temp OK = Fermeture automatique**
5. **Archive = TOUS les détails sauvegardés**

---

## ✨ C'est Prêt!

Le système est **complètement implémenté, testé et prêt à être utilisé**. 

Tous les fichiers ont été modifiés:
- ✅ `DHT/models.py` - Structure
- ✅ `DHT/signals.py` - Logique
- ✅ `DHT/api.py` - Endpoints
- ✅ `DHT/serializers.py` - Format JSON
- ✅ `DHT/urls.py` - Routes

Et les migrations ont été appliquées:
- ✅ Migration `0007_...` créée et appliquée

**Vous pouvez commencer à utiliser le système maintenant!**

