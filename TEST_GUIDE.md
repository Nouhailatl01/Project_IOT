# 🎯 GUIDE DE TEST DU SYSTÈME D'INCIDENTS

## État du serveur
✓ Serveur Django en cours d'exécution sur `http://127.0.0.1:8000/`

## 🧪 Scénarios de test

### Scenario 1: Mesure NORMALE (pas d'incident)
```bash
curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{"temp": 5.0, "hum": 60.0}'
```
**Résultat attendu:** Pas d'incident, compteur = 0

---

### Scenario 2: Mesure ANORMALE (T > 8)
```bash
curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{"temp": 15.0, "hum": 60.0}'
```
**Résultat attendu:**
- Incident créé
- Compteur = 1
- Opérateur 1 s'affiche

---

### Scenario 3: Escalade (4+ mesures anormales)
**Étapes:**
1. Envoyer 4 mesures avec T = 20°C
2. Vérifier que Opérateur 1 ET 2 s'affichent
3. Envoyer 3 mesures supplémentaires
4. Vérifier que Opérateurs 1, 2 ET 3 s'affichent

**URLs pour tester:**
- Dashboard opérateur (login requis): `http://localhost:8000/dashboard/`
- État incident: `http://localhost:8000/incident/status/`

---

### Scenario 4: Retour à la normale
**Étape:**
1. Créer un incident avec T = 20°C (5 mesures)
2. Envoyer une mesure avec T = 5°C (NORMALE)

**Résultat attendu:**
- Incident fermé (is_open = False)
- end_at défini
- Archivé automatiquement
- Archive visible sur `/incident/archive/`

---

## 🔑 Connexion opérateurs

### Credentials
- **Utilisateur:** `op1` / `op2` / `op3`
- **Mot de passe:** `password`
- **URL:** `http://localhost:8000/login/`

---

## 📊 Pages à tester

| Page | URL | Description |
|------|-----|-------------|
| Dashboard public | `/` | Mesures en temps réel |
| Login opérateur | `/login/` | Authentification |
| Dashboard opérateur | `/dashboard/` | Gestion incidents + API tester |
| Graphe température | `/graph_temp/` | Courbe des mesures |
| Graphe humidité | `/graph_hum/` | Courbe des mesures |
| Archive incidents | `/incident/archive/` | Incidents fermés |
| Détails incident | `/incident/<id>/` | Infos complètes |

---

## 🔌 Endpoints API

### Créer une mesure
```
POST /api/post
Content-Type: application/json
X-CSRFToken: <token>

{
  "temp": 15.5,
  "hum": 65.0
}
```

### Obtenir dernière mesure
```
GET /latest/
```

### État incident
```
GET /incident/status/
```

### Valider opérateur
```
POST /incident/update/
Content-Type: application/json
X-CSRFToken: <token>

{
  "op": 1,
  "ack": true,
  "comment": "Problème détecté..."
}
```

---

## ✅ Checklist de test

- [ ] Mesure normale ne crée pas d'incident
- [ ] Mesure < 2°C crée incident
- [ ] Mesure > 8°C crée incident
- [ ] Compteur augmente à chaque mesure anormale
- [ ] Op1 s'affiche si compteur >= 1
- [ ] Op2 s'affiche si compteur >= 4
- [ ] Op3 s'affiche si compteur >= 7
- [ ] Accusé de réception se sauvegarde
- [ ] Commentaire se sauvegarde
- [ ] Après refresh, infos persistent
- [ ] Mesure normale ferme l'incident
- [ ] Compteur reset après fermeture
- [ ] Incident archivé visible sur `/incident/archive/`
- [ ] Clic "Détails" montre infos complètes
- [ ] Opérateurs visibles sur page détails selon compteur
- [ ] API tester fonctionne sur dashboard

---

## 📈 Flux complet à tester

1. **Se connecter** (`op1` / `password`)
2. **Vérifier état** → Pas d'incident
3. **Envoyer T=15°C** → Incident crée, Op1 s'affiche
4. **Envoyer T=20°C** 3x → Compteur=4, Op2 s'affiche
5. **Valider Op1** → Cocher + commenter + valider
6. **Vérifier sauvegarde** → Infos persistent après F5
7. **Envoyer T=25°C** 3x → Compteur=7, Op3 s'affiche
8. **Valider Op2 et Op3** → Envoyer commentaires
9. **Envoyer T=5°C** → Incident fermé
10. **Vérifier archive** → Incident visible
11. **Cliquer "Détails"** → Voir infos + commentaires opérateurs

---

## 🐛 Dépannage

### Erreur "no access"
→ Assurer que l'utilisateur est un opérateur (table DHT_operateur)

### Commentaires non sauvegardés
→ Vérifier CSRF token
→ Vérifier console erreurs (F12)

### Incident n'apparaît pas
→ Rafraîchir (`F5`)
→ Vérifier que T < 2 ou T > 8

### Base données réinitialisée
```bash
python manage.py migrate
python -c "...créer opérateurs..."
```

---

## 📝 Notes

- Serveur: `http://127.0.0.1:8000/`
- Port: `8000`
- BDD: `db.sqlite3`
- Version Django: `5.2.7`
