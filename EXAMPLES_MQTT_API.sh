#!/bin/bash
# Exemples d'utilisation de l'API MQTT

BASE_URL="http://localhost:8000"

echo "============================================="
echo "   Exemples API REST MQTT"
echo "============================================="

# ---- 1. Vérifier le statut MQTT ----
echo ""
echo "1️⃣ Vérifier le statut MQTT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "GET /mqtt/status/"
echo ""
curl -s "${BASE_URL}/mqtt/status/" | python -m json.tool
echo ""

# ---- 2. Connecter MQTT ----
echo "2️⃣ Établir la connexion MQTT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "POST /mqtt/connect/"
echo ""
curl -s -X POST "${BASE_URL}/mqtt/connect/" \
  -H "Content-Type: application/json" \
  -d '{
    "broker": "localhost",
    "port": 1883
  }' | python -m json.tool
echo ""

# ---- 3. Publier des données de capteur ----
echo "3️⃣ Publier des données de capteur"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "POST /mqtt/publish/sensor/"
echo ""
echo "Scénario 1 - Température normale:"
curl -s -X POST "${BASE_URL}/mqtt/publish/sensor/" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25,
    "humidity": 60
  }' | python -m json.tool
echo ""

echo "Scénario 2 - Température basse (alerte):"
curl -s -X POST "${BASE_URL}/mqtt/publish/sensor/" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 3,
    "humidity": 60
  }' | python -m json.tool
echo ""

echo "Scénario 3 - Température haute (alerte):"
curl -s -X POST "${BASE_URL}/mqtt/publish/sensor/" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 40,
    "humidity": 75
  }' | python -m json.tool
echo ""

# ---- 4. Publier un incident ----
echo "4️⃣ Publier un incident via MQTT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "POST /mqtt/publish/incident/1/"
echo ""
curl -s -X POST "${BASE_URL}/mqtt/publish/incident/1/" \
  -H "Content-Type: application/json" | python -m json.tool
echo ""

# ---- 5. Vérifier le statut après publication ----
echo "5️⃣ Vérifier le statut après publication"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "GET /mqtt/status/"
echo ""
curl -s "${BASE_URL}/mqtt/status/" | python -m json.tool
echo ""

# ---- 6. Déconnecter MQTT ----
echo "6️⃣ Déconnecter MQTT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "POST /mqtt/disconnect/"
echo ""
curl -s -X POST "${BASE_URL}/mqtt/disconnect/" \
  -H "Content-Type: application/json" | python -m json.tool
echo ""

echo "============================================="
echo "   Fin des exemples"
echo "============================================="
