#!/usr/bin/env python
"""
Script de test pour envoyer des mesures à l'API
"""

import requests
import json
import time

API_URL = "http://127.0.0.1:8000/api/post"

# Exemples de test
test_cases = [
    {
        "name": "Température normale (0°C)",
        "data": {"temp": 0, "hum": 50},
        "expected": "Pas d'incident"
    },
    {
        "name": "Température basse (1°C)",
        "data": {"temp": 1, "hum": 50},
        "expected": "Pas d'incident"
    },
    {
        "name": "Température critique (3°C) - INCIDENT",
        "data": {"temp": 3, "hum": 55},
        "expected": "Incident créé"
    },
    {
        "name": "Température critique (5°C) - INCIDENT",
        "data": {"temp": 5, "hum": 60},
        "expected": "Incident continue"
    },
    {
        "name": "Température critique (8°C) - INCIDENT",
        "data": {"temp": 8, "hum": 58},
        "expected": "Incident continue"
    },
    {
        "name": "Température haute (9°C)",
        "data": {"temp": 9, "hum": 52},
        "expected": "Incident fermé"
    },
    {
        "name": "Température très haute (20°C)",
        "data": {"temp": 20, "hum": 45},
        "expected": "Pas d'incident"
    },
]

def send_measurement(temp, hum):
    """Envoyer une mesure à l'API"""
    payload = {
        "temp": temp,
        "hum": hum
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_incident_status():
    """Récupérer le statut de l'incident actuel"""
    try:
        response = requests.get("http://127.0.0.1:8000/incident/status/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    print("=" * 70)
    print("🧪 TEST D'API - ENVOI DE MESURES")
    print("=" * 70)
    print()
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print(f"  Données: Temp={test['data']['temp']}°C, Hum={test['data']['hum']}%")
        print(f"  Attendu: {test['expected']}")
        
        # Envoyer la mesure
        result = send_measurement(test['data']['temp'], test['data']['hum'])
        
        if "error" in result:
            print(f"  ❌ Erreur: {result['error']}")
        else:
            print(f"  ✓ Mesure enregistrée (ID={result.get('id', '?')})")
        
        # Récupérer le statut incident
        status = get_incident_status()
        
        if "error" in status:
            print(f"  ❌ Erreur statut: {status['error']}")
        else:
            is_open = status.get('is_open', False)
            counter = status.get('counter', 0)
            if is_open:
                print(f"  📍 Statut: INCIDENT EN COURS (compteur={counter})")
            else:
                print(f"  ✓ Statut: PAS D'INCIDENT")
        
        print()
        time.sleep(1)  # Pause entre les tests
    
    print("=" * 70)
    print("✓ Tests terminés!")
    print("=" * 70)
    print()
    print("💡 Accédez à: http://127.0.0.1:8000/login/")
    print("   Utilisateur: op1")
    print("   Mot de passe: password")

if __name__ == "__main__":
    main()
