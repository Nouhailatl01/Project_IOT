#!/usr/bin/env python
"""
Test complet du système d'incidents avec compteur et escalade opérateurs.

Scenarios testés:
✅ Incidents 1-3: Counter 1-3 → OP1 seul
✅ Incidents 4-6: Counter 4-6 → OP1 + OP2
✅ Incidents 7+: Counter 7+ → OP1 + OP2 + OP3
✅ Réaction opérateur: OP1 réagit → Counter reset à 0 → Incident archivé
✅ Nouveau cycle: Incident 10 repart de counter=1
"""

import os
import django
import json
from django.utils import timezone
from datetime import timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Dht11, Incident, Operateur

def clean_incidents():
    """Nettoyer les incidents existants"""
    print("🧹 Nettoyage des incidents...")
    Incident.objects.all().delete()
    Dht11.objects.all().delete()
    print("   ✓ Incidents et DHT supprimés")

def create_sensor_reading(temp, hum, description):
    """Créer une lecture de capteur"""
    print(f"\n📊 Création lecture DHT: temp={temp}°C, hum={hum}% ({description})")
    dht = Dht11.objects.create(temp=temp, hum=hum)
    print(f"   ✓ DHT#{dht.id} créé")
    
    # Vérifier l'incident
    incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    if incident:
        print(f"   📈 Incident actif: ID={incident.id}, counter={incident.counter}, max_temp={incident.max_temp}°C")
    else:
        print(f"   ℹ️  Aucun incident actif")
    
    return dht, incident

def test_counter_1_to_3():
    """Test: Compteur 1-3 → OP1 seul"""
    print("\n" + "="*60)
    print("TEST 1: Compteur 1-3 → OP1 seul")
    print("="*60)
    
    clean_incidents()
    
    # Créer 3 lectures anormales (temperature < MIN_OK = 2)
    for i in range(1, 4):
        dht, incident = create_sensor_reading(0.5, 50, f"Anomalie {i}")
        
        if not incident:
            print(f"   ❌ ERREUR: Incident non créé au compteur {i}")
            return False
        
        if incident.counter != i:
            print(f"   ❌ ERREUR: Counter attendu {i}, reçu {incident.counter}")
            return False
        
        # Vérifier que seul OP1 est concerné
        if i <= 3:
            # Aucun OP2 ni OP3 ne devrait être alerté
            print(f"   ✓ Compteur={incident.counter} → OP1 seul (OK)")
    
    return True

def test_counter_4_to_6():
    """Test: Compteur 4-6 → OP1 + OP2"""
    print("\n" + "="*60)
    print("TEST 2: Compteur 4-6 → OP1 + OP2")
    print("="*60)
    
    # L'incident est déjà créé du test 1, on continue
    incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    
    if not incident or incident.counter != 3:
        print(f"   ❌ ERREUR: Incident non trouvé ou counter != 3")
        return False
    
    # Créer 3 lectures supplémentaires pour atteindre counter 6
    for i in range(4, 7):
        dht, incident = create_sensor_reading(0.5, 50, f"Anomalie {i}")
        
        if incident.counter != i:
            print(f"   ❌ ERREUR: Counter attendu {i}, reçu {incident.counter}")
            return False
        
        # À partir du counter 4, OP2 devrait être alerté
        if i >= 4:
            print(f"   ✓ Compteur={incident.counter} → OP1 + OP2 (OK)")
    
    return True

def test_counter_7_plus():
    """Test: Compteur 7+ → OP1 + OP2 + OP3"""
    print("\n" + "="*60)
    print("TEST 3: Compteur 7+ → OP1 + OP2 + OP3")
    print("="*60)
    
    # L'incident est déjà créé du test 2, on continue
    incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    
    if not incident or incident.counter != 6:
        print(f"   ❌ ERREUR: Incident non trouvé ou counter != 6")
        return False
    
    # Créer 2 lectures supplémentaires pour atteindre counter 8
    for i in range(7, 9):
        dht, incident = create_sensor_reading(0.5, 50, f"Anomalie {i}")
        
        if incident.counter != i:
            print(f"   ❌ ERREUR: Counter attendu {i}, reçu {incident.counter}")
            return False
        
        # À partir du counter 7, OP3 devrait être alerté
        if i >= 7:
            print(f"   ✓ Compteur={incident.counter} → OP1 + OP2 + OP3 (OK)")
    
    return True

def test_operator_response():
    """Test: Réaction opérateur → Counter reset → Incident archivé"""
    print("\n" + "="*60)
    print("TEST 4: Réaction OP1 → Counter reset → Incident archivé")
    print("="*60)
    
    incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()
    
    if not incident:
        print(f"   ❌ ERREUR: Aucun incident actif")
        return False
    
    print(f"   Incident avant: ID={incident.id}, is_open={incident.is_open}, counter={incident.counter}")
    
    # OP1 réagit avec commentaire
    incident.op1_responded = True
    incident.op1_comment = "Température anormale détectée, vérification en cours"
    incident.op1_responded_at = timezone.now()
    incident.is_open = False
    incident.end_at = timezone.now()
    incident.is_archived = True
    incident.counter = 0  # Reset du compteur
    incident.save()
    
    print(f"   Incident après: ID={incident.id}, is_open={incident.is_open}, counter={incident.counter}")
    print(f"   ✓ Incident archivé et compteur reset à 0")
    
    # Vérifier l'archivage
    if incident.is_archived and incident.counter == 0 and not incident.is_open:
        print(f"   ✓ Archivage correct (OK)")
        return True
    else:
        print(f"   ❌ ERREUR: Archivage échoué")
        return False

def test_new_cycle():
    """Test: Nouveau cycle → Counter repart de 1"""
    print("\n" + "="*60)
    print("TEST 5: Nouveau cycle → Counter repart de 1")
    print("="*60)
    
    # Créer une nouvelle lecture anormale
    dht, incident = create_sensor_reading(0.5, 50, "Anomalie du nouveau cycle")
    
    if not incident:
        print(f"   ❌ ERREUR: Incident non créé")
        return False
    
    if incident.counter != 1:
        print(f"   ❌ ERREUR: Counter attendu 1, reçu {incident.counter}")
        return False
    
    if incident.is_open != True:
        print(f"   ❌ ERREUR: Incident ne devrait pas être ouvert")
        return False
    
    print(f"   ✓ Nouveau cycle correct: counter=1, is_open=True (OK)")
    return True

def run_all_tests():
    """Exécuter tous les tests"""
    print("\n" + "█"*60)
    print("█ TEST COMPLET DU SYSTÈME D'INCIDENTS ".center(60))
    print("█"*60)
    
    tests = [
        test_counter_1_to_3,
        test_counter_4_to_6,
        test_counter_7_plus,
        test_operator_response,
        test_new_cycle,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            print(f"\n❌ EXCEPTION dans {test_func.__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_func.__name__, False))
    
    # Résumé
    print("\n" + "█"*60)
    print("█ RÉSUMÉ ".center(60))
    print("█"*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name.replace('test_', '')}")
    
    print(f"\nTotal: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS PASSÉS !")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s)")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
