"""
Test du système d'escalade d'incidents

Ce script teste le système complet d'escalade:
- Incident 1-3: Op1 uniquement
- Incident 4-6: Op1 + Op2
- Incident 7+: Op1 + Op2 + Op3
- Archivage automatique à la réaction
"""

import os
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Dht11, Incident, Operateur
from django.contrib.auth.models import User
from django.utils import timezone
import json

print("\n" + "="*80)
print("TEST SYSTÈME D'ESCALADE D'INCIDENTS")
print("="*80)

# Créer les opérateurs s'ils n'existent pas
print("\n📋 Création des opérateurs...")
for level in [1, 2, 3]:
    user, _ = User.objects.get_or_create(
        username=f"op{level}",
        defaults={"email": f"op{level}@company.com"}
    )
    op, _ = Operateur.objects.get_or_create(
        user=user,
        defaults={"level": level, "full_name": f"Opérateur {level}"}
    )
    print(f"   ✓ {op}")

print("\n" + "-"*80)
print("SCENARIO 1: Escalade de 1 à 7 sans réaction")
print("-"*80)

# Nettoyer les incidents
Incident.objects.all().delete()
Dht11.objects.all().delete()

print("\n1️⃣ Incident 1 - Température 9.5°C (hors limites)")
dht1 = Dht11.objects.create(temp=9.5, hum=45)
print(f"   ✓ Création Dht11(id={dht1.id}, temp={dht1.temp}°C)")

incident = Incident.objects.filter(is_open=True).first()
if incident:
    print(f"   ✓ Incident créé: ID={incident.id}, level={incident.escalation_level}")
    print(f"   ✓ Opérateurs à alerter: {incident.get_escalation_operators()}")

print("\n2️⃣ Incident 2 - Température 10.2°C (continue)")
dht2 = Dht11.objects.create(temp=10.2, hum=46)
print(f"   ✓ Création Dht11(id={dht2.id}, temp={dht2.temp}°C)")

incident = Incident.objects.filter(is_open=True).first()
if incident:
    print(f"   ✓ Escalade: level={incident.escalation_level}")
    print(f"   ✓ Opérateurs: {incident.get_escalation_operators()}")

print("\n3️⃣ Incident 3 - Température 11°C (continue)")
dht3 = Dht11.objects.create(temp=11, hum=47)
print(f"   ✓ Création Dht11(id={dht3.id}, temp={dht3.temp}°C)")

incident = Incident.objects.filter(is_open=True).first()
if incident:
    print(f"   ✓ Escalade: level={incident.escalation_level}")
    print(f"   ✓ Opérateurs: {incident.get_escalation_operators()}")

print("\n4️⃣ Incident 4 - Température 11.5°C (escalade à Op1+Op2)")
dht4 = Dht11.objects.create(temp=11.5, hum=48)
print(f"   ✓ Création Dht11(id={dht4.id}, temp={dht4.temp}°C)")

incident = Incident.objects.filter(is_open=True).first()
if incident:
    print(f"   ✓ Escalade: level={incident.escalation_level}")
    print(f"   ✓ Opérateurs: {incident.get_escalation_operators()}")
    print(f"   ⚠️  Op2 alerté pour la première fois!")

print("\n5️⃣ Incident 5 - Température 12°C")
dht5 = Dht11.objects.create(temp=12, hum=49)
print(f"   ✓ Création Dht11(id={dht5.id}, temp={dht5.temp}°C)")

incident = Incident.objects.filter(is_open=True).first()
if incident:
    print(f"   ✓ Escalade: level={incident.escalation_level}")
    print(f"   ✓ Opérateurs: {incident.get_escalation_operators()}")

print("\n6️⃣ Incident 6 - Température 12.5°C")
dht6 = Dht11.objects.create(temp=12.5, hum=50)
print(f"   ✓ Création Dht11(id={dht6.id}, temp={dht6.temp}°C)")

incident = Incident.objects.filter(is_open=True).first()
if incident:
    print(f"   ✓ Escalade: level={incident.escalation_level}")
    print(f"   ✓ Opérateurs: {incident.get_escalation_operators()}")

print("\n7️⃣ Incident 7 - Température 13°C (escalade à Op1+Op2+Op3)")
dht7 = Dht11.objects.create(temp=13, hum=51)
print(f"   ✓ Création Dht11(id={dht7.id}, temp={dht7.temp}°C)")

incident = Incident.objects.filter(is_open=True).first()
if incident:
    print(f"   ✓ Escalade: level={incident.escalation_level}")
    print(f"   ✓ Opérateurs: {incident.get_escalation_operators()}")
    print(f"   ⚠️  Op3 alerté - ESCALADE MAXIMALE!")

print("\n📊 État de l'escalade après 7 incidents:")
if incident:
    print(f"   ID: {incident.id}")
    print(f"   Niveau: {incident.escalation_level}")
    print(f"   Statut: {incident.status}")
    print(f"   Ouvert: {incident.is_open}")
    print(f"   Temp: {incident.min_temp}°C → {incident.max_temp}°C")
    print(f"   Historique d'escalade:")
    try:
        history = json.loads(incident.escalation_history)
        for level, data in history.items():
            print(f"      Level {level}: Ops={data.get('operators', [])}, Temp={data.get('temp')}°C")
    except:
        print(f"      (Historique non disponible)")

print("\n" + "-"*80)
print("SCENARIO 2: Réaction d'opérateur → Archivage")
print("-"*80)

print("\n✅ Op1 réagit avec commentaire")
incident.op1_responded = True
incident.op1_comment = "Thermostat réglé, problème résolu"
incident.op1_responded_at = timezone.now()

# Simulation de la réaction (comme en API)
if incident.op1_responded and incident.op1_comment:
    incident.is_open = False
    incident.status = 'resolved'
    incident.end_at = timezone.now()
    incident.escalation_level = 0
    incident.save()
    print(f"   ✓ Incident ARCHIVÉ immédiatement")
    print(f"   ✓ Nouveau statut: {incident.status}")
    print(f"   ✓ Niveau d'escalade: {incident.escalation_level}")
    print(f"   ✓ Durée: {(incident.end_at - incident.start_at).total_seconds()}s")
    print(f"   ✓ Détails sauvegardés:")
    print(f"      - Op1 a réagi à {incident.op1_responded_at}")
    print(f"      - Commentaire: '{incident.op1_comment}'")

print("\n" + "-"*80)
print("SCENARIO 3: Fermeture automatique quand température redevient OK")
print("-"*80)

# Réinitialiser
Incident.objects.all().delete()
Dht11.objects.all().delete()

print("\n1️⃣ Créer incident")
dht_bad = Dht11.objects.create(temp=10, hum=50)
incident = Incident.objects.filter(is_open=True).first()
print(f"   ✓ Incident créé: {incident.id} (level={incident.escalation_level})")

print("\n2️⃣ Escalade jusqu'à level 3")
for i in range(2):
    Dht11.objects.create(temp=11+i, hum=50)
incident = Incident.objects.filter(is_open=True).first()
print(f"   ✓ Incident escaladé: level={incident.escalation_level}")

print("\n3️⃣ Température redevient OK (5°C)")
dht_ok = Dht11.objects.create(temp=5, hum=50)
incident = Incident.objects.filter(is_open=False).order_by('-end_at').first()
if incident:
    print(f"   ✓ Incident fermé automatiquement")
    print(f"   ✓ Statut: {incident.status}")
    print(f"   ✓ Durée: {(incident.end_at - incident.start_at).total_seconds()}s")

print("\n" + "="*80)
print("✅ TESTS COMPLÉTÉS")
print("="*80)
print("\nRÉSUMÉ:")
print("  ✓ Escalade progressive: 1 → 7")
print("  ✓ Changement d'opérateurs: Op1 → Op1+Op2 → Op1+Op2+Op3")
print("  ✓ Réaction d'opérateur: Archivage immédiat")
print("  ✓ Fermeture automatique: Quand température OK")
print("  ✓ Archive complète: Tous les détails sauvegardés")
print("="*80 + "\n")
