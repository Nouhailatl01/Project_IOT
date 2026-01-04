#!/bin/bash
# EXEMPLES DE TESTS API - SYSTÈME D'ESCALADE

# Base URL
BASE_URL="http://localhost:8000"

echo "════════════════════════════════════════════════════════════════"
echo "EXEMPLES DE TESTS API - ESCALADE D'INCIDENTS"
echo "════════════════════════════════════════════════════════════════"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. RÉCUPÉRER L'ÉTAT COURANT DE L'INCIDENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commande:"
echo 'curl -s http://localhost:8000/incident/status/ | jq'
echo ""
echo "Réponse attendue:"
echo '{
  "id": 1,
  "escalation_level": 3,
  "escalation_operators": [1],
  "status": "open",
  "is_open": true,
  "max_temp": 11.0,
  "min_temp": 9.5,
  "max_hum": 50.0,
  "min_hum": 45.0,
  "op1_responded": false,
  "op2_responded": false,
  "op3_responded": false
}'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. OPÉRATEUR 1 RÉPOND AVEC COMMENTAIRE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commande:"
echo 'curl -X POST http://localhost:8000/incident/update/ \'
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"op\": 1,
    \"responded\": true,
    \"comment\": \"Thermostat réglé à +5°C, problème résolu\"
  }' | jq"
echo ""
echo "Réponse attendue:"
echo '{
  "id": 1,
  "status": "resolved",
  "escalation_level": 0,
  "op1_responded": true,
  "op1_comment": "Thermostat réglé à +5°C, problème résolu",
  "op1_responded_at": "2026-01-04T14:35:00Z",
  "is_open": false,
  "end_at": "2026-01-04T14:35:00Z"
}'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. OPÉRATEUR 2 RÉPOND (QUAND NIVEAU >= 4)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commande:"
echo 'curl -X POST http://localhost:8000/incident/update/ \'
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"op\": 2,
    \"responded\": true,
    \"comment\": \"Chauffage vérifié et normalisé\"
  }' | jq"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. OPÉRATEUR 3 RÉPOND (QUAND NIVEAU >= 7)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commande:"
echo 'curl -X POST http://localhost:8000/incident/update/ \'
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"op\": 3,
    \"responded\": true,
    \"comment\": \"Situation critique désamorcée, système revigoré\"
  }' | jq"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. RÉACTION INCOMPLÈTE (SANS COMMENTAIRE)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commande:"
echo 'curl -X POST http://localhost:8000/incident/update/ \'
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"op\": 1,
    \"responded\": true,
    \"comment\": \"\"
  }' | jq"
echo ""
echo "Résultat:"
echo "  ❌ Incident NON archivé"
echo "  Raison: Commentaire vide"
echo "  L'escalade continue..."

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. LISTER TOUS LES INCIDENTS ARCHIVÉS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commande:"
echo 'curl -s http://localhost:8000/incident/archive/list/ | jq'
echo ""
echo "Réponse: Liste d'incidents archivés"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. DÉTAILS COMPLETS D'UN INCIDENT ARCHIVÉ"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commande:"
echo 'curl -s http://localhost:8000/incident/archive/1/ | jq'
echo ""
echo "Retourne tous les détails:"
echo "  - Historique d'escalade complet (JSON)"
echo "  - Réactions de tous les opérateurs"
echo "  - Min/Max température et humidité"
echo "  - Durée totale"
echo "  - Statut final"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "SCÉNARIO COMPLET DE TEST"
echo "════════════════════════════════════════════════════════════════"

echo ""
echo "ÉTAPE 1: Créer une anomalie (via interface ou API capteur)"
echo "  → Incident créé avec level=1"
echo "  → Op1 alerté"
echo ""

echo "ÉTAPE 2: Vérifier l'état"
echo "  curl http://localhost:8000/incident/status/ | jq"
echo ""

echo "ÉTAPE 3: Simuler d'autres anomalies (ou attendre les lectures)"
echo "  → Incident escalade vers level=2, 3, 4, ..."
echo "  → Nouveaux opérateurs alertés au niveau 4 et 7"
echo ""

echo "ÉTAPE 4: Op1 répond"
echo "  curl -X POST http://localhost:8000/incident/update/ \\"
echo "    -H 'Content-Type: application/json' -d '{\"op\": 1, \"responded\": true, \"comment\": \"Résolu\"}'"
echo ""
echo "  → Incident archivé immédiatement"
echo "  → status = 'resolved'"
echo "  → escalation_level = 0"
echo ""

echo "ÉTAPE 5: Voir l'historique"
echo "  curl http://localhost:8000/incident/archive/list/ | jq"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "NOTES IMPORTANTES"
echo "════════════════════════════════════════════════════════════════"

echo ""
echo "✅ ARCHIVAGE IMMÉDIAT:"
echo "   Dès qu'un opérateur répond avec commentaire → Incident archivé"
echo ""

echo "✅ ESCALADE PROGRESSIVE:"
echo "   Level 1-3: Op1"
echo "   Level 4-6: Op1 + Op2"
echo "   Level 7+:  Op1 + Op2 + Op3"
echo ""

echo "✅ DÉTAILS SAUVEGARDÉS:"
echo "   - Historique JSON de chaque escalade"
echo "   - Réactions de chaque opérateur"
echo "   - Données capteurs (min/max)"
echo "   - Timestamps complets"
echo ""

echo "✅ COMMENT TESTER AVEC PYTHON:"
echo ""
echo "  python manage.py shell"
echo "  from DHT.models import Dht11"
echo "  Dht11.objects.create(temp=9.5, hum=50)  # Level 1"
echo "  Dht11.objects.create(temp=10, hum=50)   # Level 2"
echo "  Dht11.objects.create(temp=11, hum=50)   # Level 3"
echo ""

echo "════════════════════════════════════════════════════════════════"

