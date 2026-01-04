# 📊 GUIDE DE TEST MANUEL

## 1️⃣ Démarrer le serveur

```bash
python manage.py runserver
```

Visitez: **http://localhost:8000/operator/**

---

## 2️⃣ Tester avec les valeurs du formulaire

### ✅ Cas 1: Température NORMALE (2-8°C)
```
Température: 5
Humidité: 50
→ Cliquer [Envoyer vers /api/post]
→ Résultat: "✓ Système Normal" (aucun opérateur)
```

### ⚠️ Cas 2: Température BASSE (< 2°C)
```
Température: 0.5
Humidité: 50
→ Cliquer [Envoyer vers /api/post]
→ Résultat: "⚠️ INCIDENT EN COURS" + "OP1" s'affiche
```

### ⚠️ Cas 3: Température HAUTE (> 8°C)
```
Température: 9.5
Humidité: 50
→ Cliquer [Envoyer vers /api/post]
→ Résultat: "⚠️ INCIDENT EN COURS" + "OP1" s'affiche
```

### 📈 Cas 4: Escalade progressive (Incidents 4-6)
```
Envoyez 3x la température 10°C
→ Après le 4e incident: "OP1 + OP2" s'affiche
→ Compteur: 4
```

### 🔴 Cas 5: Escalade complète (Incidents 7+)
```
Continuez à envoyer 10°C
→ Après le 7e incident: "OP1 + OP2 + OP3" s'affiche
→ Compteur: 7
```

---

## 3️⃣ Tester la réaction de l'opérateur

### ✅ Cas 6: OP1 réagit
```
1. Envoyez température 10°C → Incident créé
2. Dans le formulaire Opérateur 1:
   ☑ J'ai vu l'incident
   📝 Écrivez: "Thermostat réparé"
3. Cliquez [✓ Confirmer]

Résultat:
  ✓ Incident fermé
  ✓ Compteur revient à 0
  ✓ Archivé
  ✓ Nouvelle anomalie repart de counter=1
```

---

## 4️⃣ Vérifier l'archive

Allez à: **http://localhost:8000/incident/archive/**

Vous devriez voir:
- Tous les incidents fermés
- Qui a réagi (OP1/OP2/OP3)
- Leurs commentaires
- Quand ils ont réagi

---

## ❌ Cas d'erreur à ÉVITER

### ❌ Erreur 1: "Unexpected token '<'"
```
Cause: L'API retourne du HTML au lieu de JSON
Solution: Assurez-vous d'envoyer:
  - Endpoint: /api/post
  - Method: POST
  - Content-Type: application/json
  - Body: {"temp": 5, "hum": 50}
```

### ❌ Erreur 2: Compteur ne s'incrémente pas
```
Cause: Température entre 2-8°C (OK)
Solution: Envoyez température < 2 ou > 8
  - Bon: temp=1 ou temp=9
  - Mauvais: temp=5
```

### ❌ Erreur 3: OP1 n'apparaît pas
```
Cause: Counter est 0 (pas d'incident)
Solution: Créez d'abord un incident (temp < 2 ou > 8)
```

### ❌ Erreur 4: Opérateur réagit mais incident ne ferme pas
```
Cause: Checkbox NON coché OU commentaire vide
Solution: DOIT avoir les deux:
  ☑ Checkbox obligatoire
  📝 Commentaire obligatoire
  Valider seulement si les deux
```

---

## 📊 Réponses attendues

### /latest/ - Dernière lecture
```json
{
  "id": 50,
  "temperature": 5.0,
  "humidity": 50.0,
  "timestamp": "2026-01-04T10:30:00Z"
}
```

### /incident/status/ - Statut incident
```json
{
  "id": 25,
  "counter": 7,
  "is_open": true,
  "max_temp": 10.5,
  "start_at": "2026-01-04T10:25:00Z",
  "op1_responded": false,
  "op2_responded": false,
  "op3_responded": false
}
```

### /api/post - Enregistrer lecture
```
Status 201 Created
Body: {...données DHT11...}
```

---

## 🚀 Résumé

| Compteur | Affichage | Réaction |
|----------|-----------|----------|
| 0 | ✓ Normal | Aucun opérateur |
| 1-3 | ⚠️ Incident | **OP1** seul |
| 4-6 | ⚠️ Incident | **OP1 + OP2** |
| 7+ | ⚠️ CRITIQUE | **OP1 + OP2 + OP3** |

Dès que quelqu'un réagit (check + comment):
- ✅ Incident fermé
- ✅ Compteur = 0
- ✅ Archivé automatiquement
- ✅ Nouveau cycle prêt
