# 📚 Index MQTT - Guide de navigation

**Version:** 1.0 - 4 janvier 2026  
**Statut:** ✅ Implémentation complète

---

## 🎯 Démarrer ici

### Pour les impatients (5 minutes)
→ **[MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md)**
- Installation rapide du broker
- Démarrage en 5 étapes
- Tests immédiats

### Pour une compréhension complète (30 minutes)
→ **[MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md)**
- Architecture détaillée
- Configuration complète
- Scénarios de test
- Dépannage

---

## 📖 Documentation

| Document | Durée | Public | Contenu |
|----------|-------|--------|---------|
| [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md) | 5 min | Tous | Démarrage rapide |
| [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md) | 30 min | Utilisateurs | Guide complet |
| [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md) | 1h | Développeurs | 10 cas avancés |
| [MQTT_IMPLEMENTATION_CHECKLIST.md](./MQTT_IMPLEMENTATION_CHECKLIST.md) | 20 min | Tests | Checklist complète |
| [MQTT_SUMMARY.md](./MQTT_SUMMARY.md) | 10 min | Décideurs | Vue d'ensemble |
| [MQTT_IMPLEMENTATION_FINAL.md](./MQTT_IMPLEMENTATION_FINAL.md) | 5 min | Tous | Résumé d'exécution |

---

## 🔧 Fichiers techniques

### Code Python

| Fichier | Lignes | Description |
|---------|--------|-------------|
| [DHT/mqtt_client.py](./DHT/mqtt_client.py) | ~250 | Client MQTT principal |
| [DHT/api.py](./DHT/api.py) | ~150 | API REST MQTT |
| [DHT/management/commands/mqtt_listener.py](./DHT/management/commands/mqtt_listener.py) | ~75 | Service listener |
| [DHT/management/commands/mqtt_publish.py](./DHT/management/commands/mqtt_publish.py) | ~95 | Publication CLI |
| [mqtt_sensor_simulator.py](./mqtt_sensor_simulator.py) | ~200 | Simulateur de capteurs |

### Configuration

| Fichier | Section | Description |
|---------|---------|-------------|
| [projet/settings.py](./projet/settings.py#L119) | Ligne 119+ | Configuration MQTT |
| [DHT/urls.py](./DHT/urls.py#L29) | Ligne 29+ | Routes API MQTT |
| [DHT/signals.py](./DHT/signals.py#L9) | Ligne 9 | Signaux Django |

### Exemples

| Fichier | Type | Utilisation |
|---------|------|------------|
| [EXAMPLES_MQTT_API.sh](./EXAMPLES_MQTT_API.sh) | Bash | Exemples curl |
| [EXAMPLES_CURL.sh](./EXAMPLES_CURL.sh) | Bash | Autres exemples |

---

## 📊 Architecture

```
                  MQTT Broker
                 (Mosquitto)
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Capteurs      Django App    API REST
   (ESP32)      (Listener)     (HTTP)
                      │
                      ▼
                  Base de
                  données
```

---

## 🚀 Utilisation par rôle

### 🔧 Développeur
1. Lire: [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md)
2. Installer: Broker MQTT + dépendances
3. Tester: Tous les scénarios
4. Référence: [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md)

### 🏗️ Architecte
1. Vue d'ensemble: [MQTT_SUMMARY.md](./MQTT_SUMMARY.md)
2. Architecture détaillée: [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#architecture)
3. Cas avancés: [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md)

### 👨‍💼 Responsable projet
1. Résumé exécutif: [MQTT_IMPLEMENTATION_FINAL.md](./MQTT_IMPLEMENTATION_FINAL.md)
2. Vue d'ensemble: [MQTT_SUMMARY.md](./MQTT_SUMMARY.md)
3. Checklist: [MQTT_IMPLEMENTATION_CHECKLIST.md](./MQTT_IMPLEMENTATION_CHECKLIST.md)

### 🧪 Testeur QA
1. Checklist: [MQTT_IMPLEMENTATION_CHECKLIST.md](./MQTT_IMPLEMENTATION_CHECKLIST.md)
2. Scénarios: [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#scénarios-de-test)
3. Troubleshooting: [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#dépannage)

---

## 🎯 Par étapes

### Installation (15 min)
- [ ] Broker MQTT: [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md#1️⃣-installer-le-broker-mqtt)
- [ ] Dépendances: `pip install paho-mqtt`
- [ ] Configuration: [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#2-configuration-django)

### Démarrage (5 min)
- [ ] Listener: `python manage.py mqtt_listener`
- [ ] Simulateur: `python mqtt_sensor_simulator.py`
- [ ] Tests: [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md#🧪-via-l'api-rest)

### Intégration (1h)
- [ ] Capteur Arduino: [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#1️⃣-intégration-avec-des-capteurs-physiques-réels)
- [ ] Home Assistant: [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#2️⃣-intégration-avec-home-assistant)
- [ ] Notifications: [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#3️⃣-système-de-notifications-temps-réel)

### Production (2h)
- [ ] TLS/SSL: [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#🔟-sécurité-avancée-mqtt)
- [ ] Clustering: [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#8️⃣-clustering-et-haute-disponibilité)
- [ ] Monitoring: [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#9️⃣-monitoring-et-métriques-mqtt)

---

## 🔄 Topics MQTT

### Publication (Django → MQTT)
```
dht11/sensor/data      → {"temperature": 25, "humidity": 60}
dht11/incidents        → {"incident_id": 1, "status": "open"}
dht11/alerts           → {"incident_id": 1, "alert_type": "..."}
dht11/status           → {"status": "online", "timestamp": "..."}
```

### Souscription (MQTT → Django)
```
dht11/sensor/data      ← Écouter les capteurs
dht11/incidents        ← Gérer les incidents
```

**Voir:** [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#📡-topics-mqtt)

---

## 📡 API REST

### Endpoints disponibles

```
GET  /mqtt/status/
POST /mqtt/connect/
POST /mqtt/disconnect/
POST /mqtt/publish/sensor/
POST /mqtt/publish/incident/<id>/
```

**Détails:** [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#📡-topics-mqtt)  
**Exemples:** [EXAMPLES_MQTT_API.sh](./EXAMPLES_MQTT_API.sh)

---

## 💡 Cas d'usage

### Simple
```bash
# Test rapide
python mqtt_sensor_simulator.py
```
→ [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md)

### Capteur Arduino
```cpp
// Code Arduino fourni
```
→ [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#1️⃣-intégration-avec-des-capteurs-physiques-réels)

### Home Assistant
```yaml
# Configuration YAML
```
→ [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#2️⃣-intégration-avec-home-assistant)

### Production
```python
# Configuration sécurisée
```
→ [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md#🔟-sécurité-avancée-mqtt)

---

## 🆘 Aide rapide

### "Connection refused"
→ [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#erreur-connection-refused)

### "No module named paho"
→ [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#erreur-no-module-named-paho)

### Les données ne sont pas reçues
→ [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#les-messages-ne-sont-pas-reçus)

### La base de données n'est pas mise à jour
→ [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md#la-base-de-données-nest-pas-mise-à-jour)

---

## 📊 Statistiques

| Élément | Nombre |
|---------|--------|
| Fichiers Python créés | 5 |
| Fichiers Python modifiés | 4 |
| Documents Markdown | 6 |
| Lignes de code | ~1000 |
| Lignes de documentation | ~2000 |
| Endpoints API | 5 |
| Topics MQTT | 4 |
| Scénarios de test | 4+ |
| Cas avancés | 10+ |

---

## ✅ Checklist rapide

- [ ] Broker MQTT installé
- [ ] `pip install paho-mqtt`
- [ ] `python manage.py check` ✅
- [ ] `python manage.py mqtt_listener` en cours
- [ ] Simulateur teste ✅
- [ ] API REST répond ✅
- [ ] Données en BD ✅

---

## 🎓 Apprentissage progressif

### Niveau 1: Débutant (30 min)
1. [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md) - Démarrage
2. Tester le simulateur
3. Vérifier les données en BD

### Niveau 2: Intermédiaire (1h)
1. [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md) - Complète
2. Tester tous les endpoints API
3. Comprendre l'architecture

### Niveau 3: Avancé (3h)
1. [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md) - Cas complexes
2. Intégrer capteur Arduino
3. Configuration production

### Niveau 4: Expert (5h)
1. Implémenter clustering MQTT
2. Configurer TLS/SSL
3. Intégrer Home Assistant
4. Mise en place Grafana

---

## 📞 Support

### Questions?
→ Consultez [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md)

### Problèmes?
→ [Section Dépannage](./MQTT_INTEGRATION_GUIDE.md#🐛-dépannage)

### Idées d'améliorations?
→ [Prochaines étapes](./MQTT_INTEGRATION_GUIDE.md#🎯-prochaines-étapes)

---

## 🔗 Liens rapides

| Besoin | Document |
|--------|----------|
| Démarrer vite | [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md) |
| Comprendre | [MQTT_INTEGRATION_GUIDE.md](./MQTT_INTEGRATION_GUIDE.md) |
| Approfondir | [MQTT_ADVANCED_CASES.md](./MQTT_ADVANCED_CASES.md) |
| Tester | [MQTT_IMPLEMENTATION_CHECKLIST.md](./MQTT_IMPLEMENTATION_CHECKLIST.md) |
| Vue d'ensemble | [MQTT_SUMMARY.md](./MQTT_SUMMARY.md) |
| Résultat final | [MQTT_IMPLEMENTATION_FINAL.md](./MQTT_IMPLEMENTATION_FINAL.md) |

---

## 🎉 Résumé

Votre projet Django dispose maintenant d'une **intégration MQTT complète** avec:

✅ Client MQTT robuste  
✅ API REST complète  
✅ Automatisation complète  
✅ Documentation exhaustive  
✅ Simulateur de capteurs  
✅ Prêt pour production  

**Commencez par:** [MQTT_QUICKSTART.md](./MQTT_QUICKSTART.md)

---

**Index créé le:** 4 janvier 2026  
**Dernière mise à jour:** 4 janvier 2026
