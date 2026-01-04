## 📊 Dashboard Opérateurs DHT11 - Guide d'Utilisation

### 🔐 Authentification

**URL de connexion:** `http://localhost:8000/login/`

**Comptes de test disponibles:**
- `op1` / `password` - Opérateur 1
- `op2` / `password` - Opérateur 2  
- `op3` / `password` - Opérateur 3

Chaque opérateur se voit attribuer un niveau de 1 à 3.

---

### 📌 Fonctionnalités Principales

#### 1️⃣ **Mesures en Temps Réel**
- Affichage continu de la température (°C) et humidité (%)
- Rafraîchissement automatique toutes les 3 secondes
- Timestamps relatifs (il y a X secondes/minutes/heures)

#### 2️⃣ **Gestion des Incidents**
Les incidents sont détectés automatiquement quand la température est **ENTRE 2°C et 8°C** (inclus).

**États possibles:**
- **❌ Pas d'incident** - Température hors de la plage [2-8]
- **⚠️ Incident en cours** - Température détectée dans la plage [2-8]

**Escalade des opérateurs:**
| Compteur d'incidents | Opérateurs impliqués |
|---|---|
| 1+ | Opérateur 1 |
| 4+ | Opérateurs 1 + 2 |
| 7+ | Opérateurs 1 + 2 + 3 |

#### 3️⃣ **Intervention des Opérateurs**

Pour chaque incident, l'opérateur doit:

1. ✅ **Cocher l'accusé de réception** - Confirme qu'il a pris connaissance de l'incident
2. 💬 **Ajouter un commentaire** (optionnel) - Décrire les actions prises
3. 💾 **Valider** - Enregistrer son intervention

**Informations affichées après validation:**
- Date/heure de validation
- Statut de l'accusé de réception (Oui/Non)
- Commentaire enregistré

---

### 🔌 **Tester l'API (POST JSON)**

Vous pouvez envoyer manuellement une mesure vers l'API pour tester:

1. Entrez une **température** (°C)
2. Entrez une **humidité** (%)
3. Cliquez sur **"Envoyer vers /api/post"**
4. La réponse JSON s'affiche dans la zone de résultat

**Exemple de requête manuelle:**
```bash
curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -d '{"temp": 5.5, "hum": 65.0}'
```

**Réponse exemple:**
```json
{
  "id": 42,
  "temp": 5.5,
  "hum": 65.0,
  "dt": "2025-12-31T10:30:45.123456Z"
}
```

---

### 📊 **Interfaces Disponibles**

| URL | Description |
|---|---|
| `/` | Dashboard public (ancien) |
| `/login/` | Connexion opérateur |
| `/dashboard/` | Dashboard opérateur (sécurisé) |
| `/api/` | Liste toutes les mesures (API REST) |
| `/api/post` | Envoyer une nouvelle mesure (POST) |
| `/latest/` | Dernière mesure (JSON) |
| `/graph_temp/` | Graphe température |
| `/graph_hum/` | Graphe humidité |
| `/incident/status/` | Statut incident actuel (API) |
| `/incident/update/` | Mettre à jour une intervention opérateur (POST) |
| `/incident/archive/` | Archive des incidents fermés |
| `/incident/<id>/` | Détails d'un incident spécifique |

---

### 🔑 **Détails Techniques**

#### Modèle Opérateur
```python
class Operateur(models.Model):
    user = OneToOneField(User)          # Lien vers utilisateur Django
    level = IntegerField (1, 2, ou 3)   # Niveau d'opérateur
    is_active = BooleanField(True)      # Compte actif?
    created_at = DateTimeField()        # Date création
```

#### Modèle Incident
```python
class Incident(models.Model):
    start_at = DateTimeField()          # Début incident
    end_at = DateTimeField()            # Fin incident
    is_open = BooleanField()            # Ouvert?
    counter = IntegerField()            # Compteur d'alerte
    max_temp = FloatField()             # Température max détectée
    
    # Accusés de réception
    op1_ack, op2_ack, op3_ack = BooleanField()
    
    # Commentaires
    op1_comment, op2_comment, op3_comment = TextField()
    
    # Dates de validation
    op1_saved_at, op2_saved_at, op3_saved_at = DateTimeField()
```

#### Modèle Mesure
```python
class Dht11(models.Model):
    temp = FloatField()       # Température en °C
    hum = FloatField()        # Humidité en %
    dt = DateTimeField()      # Date/heure automatique
```

---

### 🛠️ **Administration Django**

Pour gérer les opérateurs via l'admin Django:

```bash
python manage.py createsuperuser
```

Puis accédez à: `http://localhost:8000/admin/`

Vous pouvez:
- Créer/modifier/supprimer des opérateurs
- Afficher l'historique des incidents
- Consulter les mesures enregistrées

---

### 📱 **Responsive Design**

L'interface est adaptée pour:
- ✅ Desktop (1024px+)
- ✅ Tablette
- ✅ Mobile

---

### 🚀 **Démarrage Rapide**

```bash
# Activer l'environnement virtuel
./venv/Scripts/Activate.ps1

# Appliquer les migrations
python manage.py migrate

# Créer les opérateurs de test
python -c "..."  # (voir commande précédente)

# Démarrer le serveur
python manage.py runserver

# Accéder à l'interface
# - Login: http://localhost:8000/login/
# - Dashboard: http://localhost:8000/dashboard/
```

---

### ❓ **Troubleshooting**

**Problème:** "Vous n'avez pas accès à ce système"
- **Solution:** Vérifiez que l'utilisateur a un profil `Operateur` associé

**Problème:** L'incident ne se ferme pas
- **Solution:** La température doit être **HORS** de la plage [2-8] pour fermer l'incident

**Problème:** Les opérateurs n'apparaissent pas
- **Solution:** Vérifiez le nombre d'incidents:
  - Op1: visible si counter ≥ 1
  - Op2: visible si counter ≥ 4
  - Op3: visible si counter ≥ 7

---

**Développé avec ❤️ Django + DRF**
