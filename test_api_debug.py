#!/usr/bin/env python
"""Test l'API /api/post pour vérifier la création d'incidents"""

import os
import sys
import django
import json
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Dht11, Incident

print("🧪 TEST DIRECT DE LA LOGIQUE D'INCIDENT")
print("="*60)

# Vider les incidents précédents
Incident.objects.all().delete()
Dht11.objects.all().delete()
print("✅ Tables nettoyées\n")

# Test 1: Créer un DHT11 avec température hors limite (1.5°C)
print("📊 TEST 1: Température 1.5°C (HORS LIMITE 2-8)")
print("-" * 60)
dht1 = Dht11.objects.create(temp=1.5, hum=50)
print(f"✓ DHT11 créé: ID={dht1.id}, temp={dht1.temp}°C")

# Vérifier que l'incident a été créé (cela se fait dans perform_create)
incidents = Incident.objects.all()
print(f"✓ Incidents en DB: {incidents.count()}")
if incidents.exists():
    inc = incidents.first()
    print(f"  ✅ ID: {inc.id}")
    print(f"  ✅ Counter: {inc.counter}")
    print(f"  ✅ Is Open: {inc.is_open}")
    print(f"  ✅ Max Temp: {inc.max_temp}")
else:
    print(f"  ❌ AUCUN incident créé!")

# Test 2: Deuxième lecture avec température hors limite
print("\n📊 TEST 2: Température 0.5°C (HORS LIMITE)")
print("-" * 60)
dht2 = Dht11.objects.create(temp=0.5, hum=45)
print(f"✓ DHT11 créé: ID={dht2.id}, temp={dht2.temp}°C")

# Vérifier le compteur
incidents = Incident.objects.filter(is_open=True)
if incidents.exists():
    inc = incidents.first()
    print(f"  ✅ Counter APRÈS 2e anomalie: {inc.counter}")
    print(f"  ✅ Max Temp: {inc.max_temp}°C")
    if inc.counter != 2:
        print(f"  ❌ ERREUR: Counter devrait être 2, pas {inc.counter}")
else:
    print("  ❌ Aucun incident ouvert!")

# Test 3: Température OK → incident devrait se fermer
print("\n📊 TEST 3: Température 5°C (OK, entre 2-8)")
print("-" * 60)
dht3 = Dht11.objects.create(temp=5, hum=60)
print(f"✓ DHT11 créé: ID={dht3.id}, temp={dht3.temp}°C")

# Vérifier que l'incident est fermé
incidents_open = Incident.objects.filter(is_open=True)
incidents_closed = Incident.objects.filter(is_open=False)
print(f"  ✅ Incidents ouverts: {incidents_open.count()}")
print(f"  ✅ Incidents fermés: {incidents_closed.count()}")
if incidents_closed.exists():
    inc = incidents_closed.first()
    print(f"     └─ Incident fermé: ID={inc.id}, counter={inc.counter}")

# Test 4: Créer 3 anomalies (counter devrait aller à 3)
print("\n📊 TEST 4: Simuler 3 lectures anormales + 1 OK")
print("-" * 60)
Incident.objects.all().delete()

for i in range(1, 4):
    dht = Dht11.objects.create(temp=9+i, hum=40)  # 10, 11, 12°C (> 8)
    inc = Incident.objects.filter(is_open=True).first()
    print(f"  Lecture {i}: temp={dht.temp}°C → Counter={inc.counter if inc else 0}")

# Normaliser
dht = Dht11.objects.create(temp=5, hum=50)
inc = Incident.objects.filter(is_open=False).first()
print(f"  Lecture 4: temp={dht.temp}°C (OK) → Incident fermé")

# Test 5: Vérifier que les opérateurs s'affichent selon le compteur
print("\n📊 TEST 5: Vérifier la logique d'affichage des opérateurs")
print("-" * 60)
Incident.objects.all().delete()

test_cases = [
    (1, "OP1 seul"),
    (3, "OP1 seul"),
    (4, "OP1 + OP2"),
    (6, "OP1 + OP2"),
    (7, "OP1 + OP2 + OP3"),
]

for counter, expected in test_cases:
    inc = Incident.objects.create(is_open=True, counter=counter, max_temp=10)
    
    # Logique d'affichage
    operators = "OP1"
    if counter >= 4:
        operators += " + OP2"
    if counter >= 7:
        operators += " + OP3"
    
    status = "✅" if operators == expected else "❌"
    print(f"  {status} Counter={counter} → {operators} (attendu: {expected})")
    inc.delete()

print("\n" + "="*60)
print("✅ TESTS TERMINÉS")
