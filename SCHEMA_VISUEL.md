# 📊 SCHÉMA VISUEL - SYSTÈME D'INCIDENTS SIMPLIFIÉ

## 🎯 Vue d'ensemble du flux

```
TEMPÉRATURE ANORMALE
        ↓
   CRÉER INCIDENT
   (counter = 1)
        ↓
   ┌────────────────────┐
   │  QUEL COMPTEUR?    │
   └────────────────────┘
        ↓
   ┌────┬────┬────┐
   ↓    ↓    ↓    ↓
  1-3  4-6  7+   ...
   │    │    │
   │    │    └─→ OP1 + OP2 + OP3
   │    └─→ OP1 + OP2
   └─→ OP1 SEUL

        ↓
   OPÉRATEUR VOIT
   FORMULAIRE
        ↓
   ┌────────────────────┐
   │ CHECKBOX: J'AI VU  │  ← DOIT être coché
   │ COMMENTAIRE: ...   │  ← DOIT être rempli
   │ [CONFIRMER]        │
   └────────────────────┘
        ↓
   SI COCHÉ + COMMENTAIRE:
   ├─ Marquer comme réagi
   ├─ Enregistrer commentaire
   ├─ Compteur = 0
   ├─ Fermer incident
   └─ Archiver
        ↓
   FIN ✅
```

---

## 📈 Exemple: Incidents successifs

```
INCIDENT 1     INCIDENT 2     INCIDENT 3
├─ counter=1   ├─ counter=2   ├─ counter=3
├─ OP1 alerté  ├─ OP1 alerté  ├─ OP1 alerté
└─ OP1 ignore  └─ OP1 ignore  └─ OP1 ignore
                                      ↓
INCIDENT 4     INCIDENT 5     INCIDENT 6
├─ counter=4   ├─ counter=5   ├─ counter=6
├─ OP1+OP2     ├─ OP1+OP2     ├─ OP1+OP2
│   alertés    │   alertés    │   alertés
└─ OP1 ignore  └─ OP2 RÉAGIT! │
                   │            │
                   ├─ ✅ Réagi  │
                   ├─ 📝 Commentaire
                   ├─ 🔄 Counter = 0
                   ├─ 🚫 Incident fermé
                   └─ 📦 Archivé
                   
                   INCIDENT 7
                   ├─ counter=1 (nouveau cycle!)
                   ├─ OP1 alerté
                   └─ ...
```

---

## 🎨 Interface utilisateur

### Cas 1: Counter 1-3 (OP1 seul)
```
┌─────────────────────────────────────┐
│ ⚠️ INCIDENT EN COURS                │
│ Compteur: 2                         │
│ Alertés: OP1                        │
├─────────────────────────────────────┤
│                                     │
│ 🟦 Opérateur 1                      │
│ ├─ Statut: ⏳ En attente            │
│ ├─ ☐ J'ai vu l'incident            │
│ ├─ [                              ] │
│ │ Décrivez l'action que vous       │
│ │ avez prise...                    │
│ └─ [CONFIRMER]                      │
│                                     │
│ 🟧 Opérateur 2 (CACHÉ)              │
│ 🟥 Opérateur 3 (CACHÉ)              │
│                                     │
└─────────────────────────────────────┘
```

### Cas 2: Counter 4-6 (OP1 + OP2)
```
┌─────────────────────────────────────┐
│ ⚠️ INCIDENT EN COURS                │
│ Compteur: 5                         │
│ Alertés: OP1 + OP2                  │
├─────────────────────────────────────┤
│                                     │
│ 🟦 Opérateur 1                      │
│ ├─ Statut: ⏳ En attente            │
│ ├─ ☐ J'ai vu l'incident            │
│ ├─ [                              ] │
│ └─ [CONFIRMER]                      │
│                                     │
│ 🟧 Opérateur 2  ← VISIBLE!          │
│ ├─ Statut: ⏳ En attente            │
│ ├─ ☐ J'ai vu l'incident            │
│ ├─ [                              ] │
│ └─ [CONFIRMER]                      │
│                                     │
│ 🟥 Opérateur 3 (CACHÉ)              │
│                                     │
└─────────────────────────────────────┘
```

### Cas 3: Counter 7+ (OP1 + OP2 + OP3)
```
┌─────────────────────────────────────┐
│ ⚠️ INCIDENT EN COURS                │
│ Compteur: 8                         │
│ Alertés: OP1 + OP2 + OP3            │
├─────────────────────────────────────┤
│ 🟦 Opérateur 1 [CONFIRMER]          │
│ 🟧 Opérateur 2 [CONFIRMER]          │
│ 🟥 Opérateur 3 [CONFIRMER] ← VISIBLE│
│                                     │
│ DÈS QUE L'UN DES 3 RÉAGIT:          │
│ → Incident fermé                    │
│ → Counter = 0                       │
│ → Archivé                           │
│                                     │
└─────────────────────────────────────┘
```

---

## 🔄 Cycle de réaction

### Opérateur reçoit notification

```
1. VOIR LE FORMULAIRE
   ↓
2. DÉCIDER DE RÉAGIR?
   ├─ Oui → Aller à 3
   └─ Non → Quitter (rien ne change)
   ↓
3. COCHER "J'ai vu"
   ↓
4. ÉCRIRE COMMENTAIRE
   "Capteur remplacé, temp OK"
   ↓
5. CLIQUER "CONFIRMER"
   ↓
6. ✅ ENREGISTRÉ!
   ├─ Commentaire sauvé
   ├─ Timestamp noté
   ├─ Incident fermé
   └─ Archivé
```

---

## 📊 État des incidents

### Ouvert
```
is_open = True
→ Formulaires actifs
→ Opérateurs peuvent réagir
→ Visible dans le dashboard
```

### Fermé
```
is_open = False
is_archived = True
→ Formulaires désactivés
→ Visible dans l'archive
→ Plus modifiable
```

---

## 🎯 Points clés

### ✅ DOIT arriver ensemble
```
┌─────────────────┐
│ CHECKBOX COCHÉ  │  +  COMMENTAIRE ÉCRIT  →  ✅ ACCEPTÉ
└─────────────────┘     OBLIGATOIRE
```

### ❌ NE marche pas seul
```
☐ CHECKBOX seul              →  ❌ REFUSÉ
   "Veuillez écrire un commentaire"

COMMENTAIRE seul             →  ❌ REFUSÉ
(sans cocher la checkbox)
   "Veuillez cocher J'ai vu l'incident"
```

---

## 📈 Statistiques

### Dashboard montre
```
✓ Compteur courant
✓ Opérateurs alertés
✓ Température max
✓ Durée de l'incident
✓ Statut (ouvert/fermé)
```

### Archive montre
```
✓ Tous les incidents fermés
✓ Qui a réagi (OP1/OP2/OP3)
✓ Quand ils ont réagi
✓ Leurs commentaires
✓ Nombre d'incidents avant résolution
```

---

## 🚀 Déploiement

### Avant de démarrer
```
☑ python manage.py migrate       (migrations appliquées)
☑ python test_new_escalation.py  (test réussi)
☑ Aucune erreur en console
```

### Démarrer le serveur
```
python manage.py runserver

Puis aller à:
✓ http://localhost:8000/operator/  (dashboard)
✓ http://localhost:8000/incident/archive/  (archive)
```

---

**Système d'incidents SIMPLIFIÉ et CLARIFIÉ**  
**✅ Testé et validé pour production**  
**📅 4 janvier 2026**
