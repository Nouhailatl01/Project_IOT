# Système d'Escalade d'Incidents

## 📋 Vue d'ensemble

Ce système gère automatiquement l'escalade des incidents en fonction du nombre de violations des seuils de température. Chaque incident a un niveau d'escalade qui détermine quels opérateurs doivent être alertés.

## 🔢 Niveaux d'Escalade

| Niveau | Opérateurs Alertés | Description |
|--------|-------------------|-------------|
| **1** | Op1 | Premier incident détecté |
| **2** | Op1 | Deuxième violation continue |
| **3** | Op1 | Troisième violation continue |
| **4** | Op1, Op2 | Quatrième violation - escalade |
| **5** | Op1, Op2 | Cinquième violation continue |
| **6** | Op1, Op2 | Sixième violation continue |
| **7+** | Op1, Op2, Op3 | Escalade maximale |

## ⚙️ Fonctionnement du Système

### 1️⃣ Détection d'Incident

Quand une lecture DHT11 détecte une **température hors limites** (< 2°C ou > 8°C):

```
Température OK
     ↓
[Lecture anomale détectée]
     ↓
Créer Incident(escalation_level=1)
Alerter Op1
```

### 2️⃣ Escalade Progressive

Tant que la température reste hors limites ET qu'aucun opérateur ne réagit:

```
Incident(level=1) + nouvelle anomalie
     ↓
Escalade à level=2
     ↓
Alerter Op1 (continuation)
```

**Ce processus continue jusqu'au niveau 7**

### 3️⃣ Réaction d'Opérateur ✅

Quand un opérateur **réagit avec commentaire** (coché + message):

```
Incident(level=5, Op1+Op2 alertés)
     ↓
Op1 répond: responded=true + comment="Problème signalé au maintenance"
     ↓
INCIDENT ARCHIVÉ IMMÉDIATEMENT
     ↓
escalation_level = 0
status = "resolved"
```

### 4️⃣ Fermeture Automatique

Quand la température **revient à normal** (entre 2°C et 8°C):

```
Incident(level=3, is_open=true)
     ↓
[Lecture de température OK]
     ↓
INCIDENT ARCHIVÉ
status = "archived"
end_at = [timestamp]
```

## 📊 Modèle de Données

### Champs Clés du Modèle Incident

```python
{
    "id": 1,
    "start_at": "2024-01-04T10:30:00Z",
    "end_at": "2024-01-04T11:45:00Z",
    "is_open": false,
    "status": "resolved",  # open, resolved, archived
    
    # Escalade
    "escalation_level": 4,  # 0-7+
    "escalation_operators": [1, 2],  # Op1, Op2 pour level 4
    "escalation_history": {
        "1": {
            "timestamp": "2024-01-04T10:30:00Z",
            "temp": 9.5,
            "hum": 45.2,
            "operators": [1],
            "message": "Incident 1 détecté - Alerter Op1"
        },
        "2": {
            "timestamp": "2024-01-04T10:31:00Z",
            "temp": 10.2,
            "operators": [1],
            "message": "Incident 2 - Alerter Op1"
        }
    },
    
    # Données capteurs
    "max_temp": 11.5,
    "min_temp": 9.0,
    "max_hum": 65.0,
    "min_hum": 35.0,
    
    # Réactions Op1
    "op1_responded": true,
    "op1_comment": "Thermostat réglé à +5°C",
    "op1_responded_at": "2024-01-04T10:45:00Z",
    
    # Réactions Op2
    "op2_responded": false,
    "op2_comment": null,
    "op2_responded_at": null,
    
    # Réactions Op3
    "op3_responded": false,
    "op3_comment": null,
    "op3_responded_at": null,
    
    # Détails spéciaux
    "is_product_lost": false,  # true si 10h sans réaction
    "duration": 4500,  # en secondes
    "is_resolved": true
}
```

## 🔄 Flux Complet d'un Incident

```
┌─────────────────────────────────────────────────────────────────┐
│                    DÉTECTION DE L'INCIDENT                      │
│  Température = 9.5°C (hors limites 2-8)                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Incident créé                                                   │
│  - escalation_level = 1                                          │
│  - Alerter: Op1                                                  │
│  - max_temp = 9.5°C                                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴──────────┐
                    │                    │
          [ESCALADE]│                    │[RÉACTION]
                    │                    │
                    ↓                    ↓
            Nouvelle anomalie      Op1 répond avec
            (temp 10.2°C)          commentaire
                    │                    │
                    ↓                    ↓
        escalation_level = 2      ┌───────────────┐
        Alerter: Op1              │ INCIDENT      │
                    │              │ ARCHIVÉ       │
            ... continue ...       │ resolved      │
                    │              │ level = 0     │
            escalation_level = 4   └───────────────┘
            Alerter: Op1, Op2
                    │
                    ↓
        [Nouveau incident ou]
        [Température redevient OK]
                    │
                    ↓
        ┌───────────────────────┐
        │ INCIDENT ARCHIVÉ      │
        │ status = archived     │
        │ Tous les détails      │
        │ sauvegardés           │
        └───────────────────────┘
```

## 🛡️ Scénarios Spéciaux

### Scénario 1: Escalade Maximale atteinte (Level 7)

```
Si l'incident atteint level 7 et les 3 opérateurs ont été alertés:

level=7: Op1, Op2, Op3 tous alertés
         ↓
    Si personne ne réagit → Continue à level 7
    (relance les alertes pour Op1, Op2, Op3)
```

### Scénario 2: Produit Perdu

```
Incident ouvert depuis > 10 heures
+ AUCUNE réaction d'opérateur

→ is_product_lost = true
→ Alerte spéciale
```

### Scénario 3: Température Revient à Normal

```
Incident(level=4, open=true)
     ↓
[Lecture: temp = 5.5°C (OK)]
     ↓
INCIDENT FERMÉ ET ARCHIVÉ
- status = "archived"
- is_open = false
- end_at = [timestamp]
```

## 📡 Endpoints API

### 1. Récupérer l'état courant
```
GET /incident/status/

Retour:
{
    "id": 1,
    "escalation_level": 4,
    "escalation_operators": [1, 2],
    "status": "open",
    ...
}
```

### 2. Mettre à jour réaction opérateur
```
POST /incident/update/

Body:
{
    "op": 1,
    "responded": true,
    "comment": "Problème résolu, thermostat réglé"
}

Retour: Incident archivé (level=0)
```

### 3. Lister les incidents archivés
```
GET /incident/archive/list/

Retour: Liste de tous les incidents résolus/archivés
```

### 4. Détails d'un incident archivé
```
GET /incident/archive/<id>/

Retour: Tous les détails avec historique complet
```

## 💾 Archive - Détails Sauvegardés

Quand un incident est archivé, tous ces détails sont conservés:

✅ **Données Capteurs:**
- Température: min, max
- Humidité: min, max

✅ **Historique d'Escalade:**
- Chaque niveau avec timestamp
- Opérateurs alertés à chaque niveau
- État des capteurs à chaque escalade

✅ **Réactions Opérateurs:**
- Qui a réagi (Op1/Op2/Op3)
- Quand ils ont réagi (timestamp)
- Leurs commentaires complets

✅ **Métadonnées:**
- Durée totale de l'incident
- Statut final (resolved/archived)
- Si produit perdu

## 🚀 Améliorations Implémentées

1. ✅ **Escalade Progressive**: De 0 à 7+ niveaux
2. ✅ **Opérateurs Multiples**: Op1 seul → Op1+Op2 → Op1+Op2+Op3
3. ✅ **Archivage Complet**: Tous les détails conservés
4. ✅ **Historique JSON**: Trace complète de l'escalade
5. ✅ **Réaction Immédiate**: Archive l'incident dès réaction
6. ✅ **Fermeture Automatique**: Si température OK
7. ✅ **Produit Perdu**: Détection après 10h d'inactivité

