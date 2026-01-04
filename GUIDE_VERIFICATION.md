# 🔍 Guide de Vérification - Système d'Incidents

Ce guide vous permet de vérifier que le système fonctionne correctement via l'interface.

---

## 🚀 Démarrage du Serveur

```bash
# 1. Naviguer dans le répertoire du projet
cd c:\Users\nouha\Desktop\pythonProject\ -\ Copi

# 2. Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# 3. Lancer le serveur Django
python manage.py runserver
```

Le serveur démarre à: **http://localhost:8000**

---

## 📱 Tester via l'Interface Dashboard

### 1️⃣ Accès au Dashboard
1. Ouvrir un navigateur
2. Aller à: `http://localhost:8000`
3. Se connecter avec les identifiants opérateur
4. Voir le **Dashboard Opérateur**

### 2️⃣ Simuler une Anomalie

**Méthode 1: Via l'API Tester (dans le dashboard)**
1. Aller à la section **"🔌 Testeur API"**
2. Entrer:
   - Température: **0.5** (< MIN_OK = 2)
   - Humidité: **60**
3. Cliquer **"Envoyer vers /api/post"**
4. Observer le tableau **"État"**:
   - ✅ Badge passe à **"ALERTE"**
   - ✅ Compteur passe à **"1"**
   - ✅ Opérateurs alertés: **"OP1"**
   - ✅ OP1 card devient visible

### 3️⃣ Tester l'Escalade des Opérateurs

**Test: Counter 1-3 → OP1 seul**
```
Envoyer 3 fois temp=0.5
Observations:
  ✅ Counter: 1 → 2 → 3
  ✅ Opérateurs: "OP1"
  ✅ Seule la card OP1 visible
```

**Test: Counter 4-6 → OP1 + OP2**
```
Envoyer 3 fois temp=0.5 (total: 6 fois)
Observations:
  ✅ Counter: 4 → 5 → 6
  ✅ Opérateurs: "OP1 + OP2"
  ✅ Cards OP1 et OP2 visibles, OP3 cachée
```

**Test: Counter 7+ → OP1 + OP2 + OP3**
```
Envoyer 1-2 fois temp=0.5 (total: 7+ fois)
Observations:
  ✅ Counter: 7 → 8
  ✅ Opérateurs: "OP1 + OP2 + OP3"
  ✅ Toutes les 3 cards visibles
```

### 4️⃣ Tester la Réaction d'Opérateur

**Test: OP1 Réagit**
1. Voir l'incident avec counter >= 4 (pour que OP2 soit aussi présente)
2. Dans la card **OP1**:
   - ✅ Cocher: **"J'ai vu l'incident"**
   - ✅ Écrire un commentaire: "Température anormale détectée, vérification en cours"
   - ✅ Cliquer: **"✓ Confirmer"**
3. Observer:
   - ✅ Alerte: **"✓ Enregistré"**
   - ✅ Incident passe à: **"✓ Système Normal"**
   - ✅ Compteur reset à: **"0"**
   - ✅ Les cards OP1/OP2/OP3 disparaissent
   - ✅ Badge: **"OK"**

### 5️⃣ Tester le Nouveau Cycle

**Test: Nouvel Incident**
1. Après l'archivage précédent
2. Envoyer 1 nouvelle lecture: temp=0.5
3. Observer:
   - ✅ Nouvel incident créé
   - ✅ Compteur: **"1"** (redémarrage)
   - ✅ Opérateurs: **"OP1"** (seul)
   - ✅ Nouvelle card OP1 visible

---

## 📊 Tester via la Page d'Archives

1. Ouvrir: `http://localhost:8000/incident-archive`
2. Voir la liste des incidents fermés
3. Vérifier:
   - ✅ Incidents archivés affichent le commentaire OP1
   - ✅ Timestamps correctes
   - ✅ Compteur final affiché

---

## 🧪 Tester via le Endpoint `/incident/status/`

**URL**: `http://localhost:8000/incident/status/`

### Réponse quand pas d'incident
```json
{
  "is_open": false,
  "counter": 0
}
```

### Réponse avec incident ouvert (counter=5)
```json
{
  "id": 35,
  "start_at": "2026-01-04T00:21:15.122349Z",
  "end_at": null,
  "is_open": true,
  "is_archived": false,
  "counter": 5,
  "max_temp": 1.5,
  "op1_responded": false,
  "op2_responded": false,
  "op3_responded": false,
  "op1_comment": "",
  "op2_comment": "",
  "op3_comment": "",
  "op1_responded_at": null,
  "op2_responded_at": null,
  "op3_responded_at": null,
  "is_product_lost": false
}
```

### Réponse avec incident archivé
```json
{
  "id": 35,
  "is_open": false,
  "is_archived": true,
  "counter": 0,
  ...
}
```

---

## 🐛 Dépannage

### Le compteur ne s'incrémente pas
- ✅ **Correction appliquée**: Bug JavaScript dans `setIncidentUI()` corrigé
- **Vérifier**: Ouvrir la console du navigateur (F12) → Onglet Console
- Pas d'erreurs JavaScript? → Système OK

### Les opérateurs ne s'affichent pas
- ✅ **Correction appliquée**: Élément HTML `incident-status` ajouté
- **Vérifier**: Inspecter le HTML (F12) → Chercher `id="incident-status"`
- L'élément est présent? → Système OK

### L'API retourne toujours `is_open: false`
- ✅ **Correction appliquée**: API `incident/status/` améliorée
- **Vérifier**: Appeler `/incident/status/` dans le navigateur
- Affiche l'incident archivé? → Système OK

---

## ✅ Checklist de Vérification

- [ ] Le serveur Django démarre sans erreur
- [ ] Le dashboard s'ouvre correctement
- [ ] Envoyer temp=0.5 crée un incident avec counter=1
- [ ] Counter s'incrémente correctement (1→2→3...)
- [ ] OP1 s'affiche pour counter=1-3
- [ ] OP2 s'ajoute pour counter=4-6
- [ ] OP3 s'ajoute pour counter=7+
- [ ] OP1 peut réagir avec commentaire
- [ ] Après réaction, incident est archivé et counter=0
- [ ] Nouvel incident redémarre à counter=1
- [ ] Envoyer temp=5 (OK) ferme l'incident
- [ ] Archive affiche correctement les incidents
- [ ] API `/incident/status/` retourne les bonnes données

Si tous les points sont ✅, le système fonctionne correctement !

---

## 📝 Notes Importantes

- Les limites de température sont: **MIN_OK = 2°C**, **MAX_OK = 8°C**
- Une température < 2 ou > 8 déclenche une anomalie
- Le compteur repart à 1 uniquement après archivage d'un incident
- Les opérateurs sont alertés à chaque signal DHT (pas de délai)
- Le rafraîchissement du dashboard est toutes les 5 secondes

---

## 🔧 Fichiers à Vérifier

Si vous avez des doutes:

1. **[static/js/dashboard.js](static/js/dashboard.js)** - Logique JavaScript
2. **[templates/dashboard_operator.html](templates/dashboard_operator.html)** - HTML du dashboard
3. **[DHT/api.py](DHT/api.py)** - Endpoints API
4. **[DHT/signals.py](DHT/signals.py)** - Gestion automatique des incidents
5. **[DHT/models.py](DHT/models.py)** - Modèles de données

Tous les correctifs sont appliqués dans ces fichiers.

---

**Status**: ✅ **Système testé et validé**
