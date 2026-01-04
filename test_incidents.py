#!/usr/bin/env python
"""
Script de test du système d'incidents
Générer différents scénarios de température pour tester la logique
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()1

from DHT.models import Dht11, Incident
from django.utils import timezone

print("=" * 60)
print("🧪 TEST DU SYSTÈME D'INCIDENTS")
print("=" * 60)

# Menu
print("\nChoisir un scénario de test:")
print("1. Créer des mesures NORMALES (T = 5°C)")
print("2. Créer des mesures ANORMALES (T = 15°C)")
print("3. Créer des mesures TRÈS ANORMALES (T = 20°C)")
print("4. Créer un incident complet (escalade)")
print("5. Afficher état actuel incident")
print("6. Réinitialiser tous les tests")
print()

choice = input("Choix (1-6): ").strip()

def create_measurement(temp, hum=60):
    """Créer une mesure"""
    m = Dht11.objects.create(temp=temp, hum=hum)
    print(f"  ✓ Créé: T={temp}°C, H={hum}%")
    return m

def show_incident_status():
    """Afficher l'état de l'incident actuel"""
    incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    
    print("\n📊 ÉTAT INCIDENT:")
    if not incident:
        print("  ✓ Aucun incident ouvert")
    else:
        print(f"  ID: #{incident.id}")
        print(f"  Compteur: {incident.counter}")
        print(f"  Temp max: {incident.max_temp}°C")
        print(f"  Début: {incident.start_at}")
        print(f"  Op1: ACK={incident.op1_ack}, Comm='{incident.op1_comment[:30]}...'")
        print(f"  Op2: ACK={incident.op2_ack}, Comm='{incident.op2_comment[:30]}...'")
        print(f"  Op3: ACK={incident.op3_ack}, Comm='{incident.op3_comment[:30]}...'")

if choice == "1":
    print("\n✓ Créer 3 mesures NORMALES (T=5°C)")
    print("  La température 5°C est DANS la plage [2-8] → PAS d'incident")
    for i in range(3):
        create_measurement(5.0)
    show_incident_status()

elif choice == "2":
    print("\n✓ Créer 5 mesures ANORMALES (T=15°C)")
    print("  La température 15°C est > 8 → INCIDENT")
    for i in range(5):
        create_measurement(15.0)
    show_incident_status()

elif choice == "3":
    print("\n✓ Créer 10 mesures TRÈS ANORMALES (T=25°C)")
    print("  La température 25°C est > 8 → INCIDENT GRAVE")
    for i in range(10):
        create_measurement(25.0)
    show_incident_status()

elif choice == "4":
    print("\n✓ Créer un incident complet avec escalade")
    print("  1. Mesures anormales → Incident + Op1")
    print("  2. Plus de mesures → Op2 apparaît")
    print("  3. Encore plus → Op3 apparaît")
    print()
    
    # Créer incident
    for i in range(2):
        create_measurement(0.5)  # < 2°C
    print("  → Opérateur 1 s'affiche (compteur=2)")
    
    for i in range(3):
        create_measurement(-5.0)
    print("  → Opérateur 1 toujours (compteur=5)")
    print("  → Opérateur 2 s'affiche (compteur>=4)")
    
    for i in range(3):
        create_measurement(-10.0)
    print("  → Opérateur 3 s'affiche (compteur>=7)")
    
    show_incident_status()
    
    # Valider les opérateurs
    incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    if incident:
        incident.op1_ack = True
        incident.op1_comment = "Alerte détectée, je m'en charge"
        incident.op1_saved_at = timezone.now()
        incident.save()
        print("\n  ✓ Opérateur 1 a validé")

elif choice == "5":
    print()
    show_incident_status()
    
    # Afficher tous les incidents
    all_incidents = Incident.objects.all().order_by("-start_at")
    print(f"\n📋 TOTAL: {all_incidents.count()} incidents")
    for inc in all_incidents[:5]:
        status = "OUVERT" if inc.is_open else "FERMÉ"
        print(f"  #{inc.id}: {status}, compteur={inc.counter}, temp_max={inc.max_temp}°C")

elif choice == "6":
    print("\n🗑️  Réinitialiser les tests")
    Dht11.objects.all().delete()
    Incident.objects.all().delete()
    print("  ✓ Tous les tests supprimés")

else:
    print("❌ Choix invalide")

print("\n" + "=" * 60)
print("✓ Test terminé")
print("=" * 60)
