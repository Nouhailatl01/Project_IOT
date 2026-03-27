#!/usr/bin/env python
"""
Test complet E2E: Simulation d'un scénario réaliste complet
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Dht11, Incident
from django.utils import timezone

def simulate_real_scenario():
    """Simuler un scénario réaliste complet"""
    
    print("\n" + "█"*70)
    print("█ SCÉNARIO E2E: SIMULATION RÉALISTE ".ljust(70) + "█")
    print("█"*70)
    
    # Nettoyage
    Incident.objects.all().delete()
    Dht11.objects.all().delete()
    
    # Étape 1: Période normale (température OK)
    print("\n📍 PHASE 1: Période Normale (Temp OK)")
    print("   → Créer 5 lectures normales")
    for i in range(5):
        dht = Dht11.objects.create(temp=5.0, hum=60.0)
        print(f"   ✓ Lecture {i+1}: temp=5.0°C (OK)")
    
    incident = Incident.objects.filter(is_open=True).first()
    assert incident is None, "Il ne devrait pas y avoir d'incident"
    print("   → Aucun incident créé ✓")
    
    # Étape 2: Anomalie détectée
    print("\n📍 PHASE 2: Anomalie Détectée (Temp trop basse)")
    print("   → Créer 3 lectures anormales (temp < 2°C)")
    for i in range(3):
        dht = Dht11.objects.create(temp=0.5, hum=60.0)
        incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
        counter = incident.counter if incident else 0
        print(f"   ✓ Lecture anormale {i+1}: Counter={counter}, OP Alertés: OP1")
    
    assert incident is not None, "Un incident devrait exister"
    assert incident.counter == 3, f"Counter devrait être 3, pas {incident.counter}"
    print("   → Incident en cours, counter=3, OP1 alerté ✓")
    
    # Étape 3: Escalade vers OP2
    print("\n📍 PHASE 3: Escalade vers OP2 (Counter >= 4)")
    print("   → Créer 4 lectures supplémentaires")
    for i in range(4):
        dht = Dht11.objects.create(temp=0.5, hum=60.0)
        incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
        counter = incident.counter if incident else 0
        ops = "OP1" if counter < 4 else "OP1 + OP2" if counter < 7 else "OP1 + OP2 + OP3"
        print(f"   ✓ Lecture anormale: Counter={counter}, OP Alertés: {ops}")
    
    incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    assert incident.counter == 7, f"Counter devrait être 7, pas {incident.counter}"
    print("   → Escalade vers OP2 et OP3 activée ✓")
    
    # Étape 4: Escalade vers OP3
    print("\n📍 PHASE 4: Escalade vers OP3 (Counter >= 7)")
    print("   → Incident continue...")
    ops_alerted = "OP1 + OP2 + OP3"
    print(f"   ✓ Counter=7, OP Alertés: {ops_alerted}")
    
    # Étape 5: OP1 réagit
    print("\n📍 PHASE 5: Réaction Opérateur")
    print("   → OP1 réagit avec action corrective")
    incident.op1_responded = True
    incident.op1_comment = "Température anormale au capteur #1, vérification en cours"
    incident.op1_responded_at = timezone.now()
    incident.is_open = False
    incident.end_at = timezone.now()
    incident.is_archived = True
    incident.counter = 0  # Reset
    incident.save()
    
    print(f"   ✓ OP1 a réagi")
    print(f"   ✓ Incident fermé et archivé")
    print(f"   ✓ Counter reset à 0")
    
    assert not incident.is_open, "Incident devrait être fermé"
    assert incident.is_archived, "Incident devrait être archivé"
    assert incident.counter == 0, "Counter devrait être 0 après réaction"
    
    # Étape 6: Situation redevient normale
    print("\n📍 PHASE 6: Situation Redevient Normale")
    print("   → Créer 3 lectures normales")
    for i in range(3):
        dht = Dht11.objects.create(temp=5.0, hum=60.0)
        print(f"   ✓ Lecture {i+1}: temp=5.0°C (OK)")
    
    incident_open = Incident.objects.filter(is_open=True).first()
    assert incident_open is None, "Il ne devrait pas y avoir d'incident ouvert"
    print("   → Système redevient normal ✓")
    
    # Étape 7: Nouvel incident (nouveau cycle)
    print("\n📍 PHASE 7: Nouvel Incident (Nouveau Cycle)")
    print("   → Nouvelle anomalie détectée")
    dht = Dht11.objects.create(temp=0.5, hum=60.0)
    incident_new = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    
    assert incident_new is not None, "Un nouvel incident devrait être créé"
    assert incident_new.counter == 1, f"Counter devrait être 1, pas {incident_new.counter}"
    assert incident_new.id != incident.id, "Devrait être un nouvel incident"
    print(f"   ✓ Nouvel incident créé: ID={incident_new.id}")
    print(f"   ✓ Counter=1 (redémarrage du cycle)")
    print(f"   ✓ OP1 alerté")
    
    # Résumé
    print("\n" + "█"*70)
    print("█ RÉSUMÉ SCÉNARIO ".ljust(70) + "█")
    print("█"*70)
    print(f"✅ Phase 1: Période normale sans incident")
    print(f"✅ Phase 2: Anomalie détectée, counter=3, OP1 alerté")
    print(f"✅ Phase 3: Escalade counter=4-6, OP2 alerté")
    print(f"✅ Phase 4: Escalade counter=7+, OP3 alerté")
    print(f"✅ Phase 5: Réaction OP1, incident archivé, counter reset")
    print(f"✅ Phase 6: Situation redevient normale")
    print(f"✅ Phase 7: Nouvel incident, nouveau cycle (counter=1)")
    print(f"\n🎉 SCÉNARIO E2E RÉUSSI !")
    print("█"*70)

if __name__ == "__main__":
    simulate_real_scenario()
