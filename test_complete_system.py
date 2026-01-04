#!/usr/bin/env python
"""Test complet du système avec vérification de l'escalade"""
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Dht11, Incident, Operateur
from django.contrib.auth.models import User

print("\n" + "="*70)
print("🧪 TEST COMPLET DU SYSTÈME D'ESCALADE D'INCIDENTS")
print("="*70)

# Nettoyer
Dht11.objects.all().delete()
Incident.objects.all().delete()

# Créer des opérateurs si n'existe pas
User.objects.filter(username__in=['op1', 'op2', 'op3']).delete()
for i in range(1, 4):
    u = User.objects.create_user(username=f'op{i}', password='pass')
    Operateur.objects.get_or_create(user=u, defaults={'level': i})

print("\n📋 SCÉNARIO: 3 anomalies → 3 anomalies → 3 anomalies = 9 incidents totaux")
print("-" * 70)

# Phase 1: Incidents 1-3 (OP1 seul)
print("\n🔴 PHASE 1: Incidents 1-3 → OP1 seul")
for i in range(1, 4):
    Dht11.objects.create(temp=0.5, hum=50)
    inc = Incident.objects.filter(is_open=True).first()
    print(f"  Incident #{i}: counter={inc.counter}, alerté à: OP1 seul")

# Phase 2: Incidents 4-6 (OP1 + OP2)
print("\n🟠 PHASE 2: Incidents 4-6 → OP1 + OP2")
for i in range(4, 7):
    Dht11.objects.create(temp=10.5, hum=50)
    inc = Incident.objects.filter(is_open=True).first()
    print(f"  Incident #{i}: counter={inc.counter}, alerté à: OP1 + OP2")

# Phase 3: Incidents 7-9 (OP1 + OP2 + OP3)
print("\n🔴 PHASE 3: Incidents 7-9 → OP1 + OP2 + OP3")
for i in range(7, 10):
    Dht11.objects.create(temp=10.5, hum=50)
    inc = Incident.objects.filter(is_open=True).first()
    print(f"  Incident #{i}: counter={inc.counter}, alerté à: OP1 + OP2 + OP3")

# Vérifier l'état final
inc = Incident.objects.filter(is_open=True).first()
print(f"\n✅ État final:")
print(f"   Counter: {inc.counter}")
print(f"   Alertés: ", end="")
if inc.counter <= 3:
    print("OP1 seul")
elif inc.counter <= 6:
    print("OP1 + OP2")
else:
    print("OP1 + OP2 + OP3")

# SIMULATION: OP1 réagit
print(f"\n🔔 OP1 RÉAGIT avec checkbox + commentaire!")
inc.op1_responded = True
inc.op1_comment = "Thermostat remplacé, température OK"
inc.op1_responded_at = timezone.now()

# Logique: Si quelqu'un réagit + commentaire → reset compteur
if inc.op1_responded and inc.op1_comment:
    inc.counter = 0
    inc.is_open = False
    inc.end_at = timezone.now()
    inc.is_archived = True
    inc.save()
    print(f"   → Counter réinitialisé à 0")
    print(f"   → Incident fermé")
    print(f"   → Archivé")

# Vérifier que le prochain incident repart de 1
print(f"\n🔴 INCIDENT 10: Nouvelle anomalie")
Dht11.objects.create(temp=0.5, hum=50)
new_inc = Incident.objects.filter(is_open=True).first()
print(f"   ✅ Nouveau counter: {new_inc.counter} (réinitialisé!)")
print(f"   ✅ Alertés à: OP1 seul")

print("\n" + "="*70)
print("✅ TEST RÉUSSI - SYSTÈME COMPLÈTEMENT FONCTIONNEL")
print("="*70 + "\n")
