# 🚀 GUIDE D'UTILISATION - SYSTÈME D'ESCALADE D'INCIDENTS

## ✅ Vérifier que tout fonctionne

### 1. Vérifier les migrations
```bash
python manage.py migrate
# Output: "Applying DHT.0005_incident_escalation_system... OK"
```

### 2. Tester le système
```bash
python test_escalation.py
# Doit afficher: "✓ TEST RÉUSSI - Le système d'escalade fonctionne correctement!"
```

### 3. Démarrer le serveur
```bash
python manage.py runserver
```

---

## 📱 Interface opérateur

### Dashboard en direct
**URL:** `http://localhost:8000/operator/`

**Affichage:**
- **Température/Humidité actuelles**
- **État de l'incident** avec niveau d'escalade
- **Formulaires pour chaque opérateur**

---

## 👤 Comment utiliser en tant qu'opérateur

### 1. Vous recevez une alerte
- Un incident s'affiche dans votre dashboard
- Vous voyez: "Incident: Escalade OP1 (1/3)"

### 2. Vous avez 3 alertes pour réagir
- **Alerte 1:** Compteur affiche "1/3"
- **Alerte 2:** Compteur affiche "2/3"  
- **Alerte 3:** Compteur affiche "3/3"
- Si vous n'avez pas réagi → **ESCALADE vers OP2**

### 3. Vous décidez de réagir
1. Cochez la case **"Réagi"**
2. Écrivez un **commentaire** décrivant vos actions:
   ```
   "Capteur remplacé. Température stabilisée à 5°C. 
    Incident résolu. Retour à la normale."
   ```
3. Cliquez sur **"Valider et sauvegarder"**

### 4. L'incident se ferme
- ✅ Compteur réinitialisé à 0
- ✅ Incident archivé avec votre commentaire
- ✅ Timestamp de votre réaction enregistré

---

## 🔄 Scénario d'escalade complète

### OP1 ne réagit pas
```
Incident 1 → OP1 alerté (1/3) - Pas de réaction
Incident 2 → OP1 alerté (2/3) - Pas de réaction
Incident 3 → OP1 alerté (3/3) - Pas de réaction
          → ESCALADE! Passage à OP2
```

### OP2 est alerté
```
Incident 4 → OP2 alerté (1/3) - OP2 voit une alerte
           → OP2 répond avec commentaire
           → Incident fermé et archivé
```

---

## 📊 Archive des incidents

### Accéder à l'archive
**URL:** `http://localhost:8000/incident/archive/`

### Voir les détails
- Cliquez sur un incident pour voir:
  - Température max, compteur
  - Commentaires de tous les opérateurs
  - Timestamps de réaction
  - Niveau d'escalade atteint

---

## ❌ Problèmes courants et solutions

### ❌ "Je ne peux pas envoyer mon commentaire"
**Solution:** 
- Assurez-vous que la case "Réagi" est cochée
- Écrivez au moins 1 caractère dans le commentaire
- Cliquez sur "Valider et sauvegarder"

### ❌ "Le formulaire ne s'enregistre pas"
**Solution:**
- Vérifiez votre connexion internet
- Rechargez la page (F5)
- Vérifiez que vous êtes connecté

### ❌ "Je vois OP2 mais je suis OP1"
**Solution:**
- C'est normal! Vous voyez tous les niveaux d'escalade
- Seul votre niveau est actif pour votre réaction

---

## 🛠️ Configuration avancée

### Modifier le délai d'escalade (actuellement 3 alertes)

**Fichier:** `DHT/api.py`

Cherchez cette ligne:
```python
if incident.escalation_counter >= 3 and incident.current_escalation_level < 3:
```

Changez `3` en un autre nombre (ex: 2 pour escalade après 2 alertes)

### Modifier le délai de perte de produit (actuellement 10h)

**Fichier:** `DHT/api.py`

Cherchez cette ligne:
```python
time_limit = incident.start_at + timedelta(hours=10)
```

Changez `hours=10` en un autre nombre (ex: `hours=6` pour 6h)

---

## 📝 Checklist avant mise en production

- [ ] Base de données migrée (`python manage.py migrate`)
- [ ] Test d'escalade réussi (`python test_escalation.py`)
- [ ] Serveur démarré sans erreurs
- [ ] Dashboard accessible
- [ ] Formulaire fonctionnel (test avec un opérateur)
- [ ] Archive accessible et fonctionnelle
- [ ] Opérateurs créés et actifs dans l'admin

---

## 🔐 Sécurité

### Accès réservé aux opérateurs
- Seuls les utilisateurs avec un profil `Operateur` actif peuvent accéder
- Authentification requise pour toutes les pages
- CSRF protection activée

### Données archivées
- Tous les commentaires sont conservés
- Aucune suppression possible
- Audit trail complet

---

## 📞 Support

Pour toute question:
1. Vérifiez les logs: `python manage.py shell`
2. Relancez le test: `python test_escalation.py`
3. Vérifiez la configuration: `python manage.py showmigrations DHT`

---

**Dernière mise à jour:** 4 janvier 2026  
**Statut du système:** ✅ OPÉRATIONNEL
