#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Incident, Dht11

def test_incident_flow():
    """Test complet du flux d'incidents"""
    
    print("\n" + "="*60)
    print("TEST COMPLET - DETECTION D'INCIDENTS")
    print("="*60)
    
    # Test 1: Mesure OK (T > 8)
    print("\n1. Envoi T=15 C (OK - pas d'incident)")
    obj1 = Dht11.objects.create(temp=15, hum=50)
    status = Incident.objects.filter(is_open=True).first()
    print(f"   Incident ouvert: {bool(status)}")
    print(f"   Mesures: {Dht11.objects.count()}")
    
    # Test 2: Incident (2 <= T <= 8)
    print("\n2. Envoi T=5 C (INCIDENT - entre 2 et 8)")
    obj2 = Dht11.objects.create(temp=5, hum=50)
    status = Incident.objects.filter(is_open=True).first()
    print(f"   Incident ouvert: {bool(status)}")
    if status:
        print(f"   Compteur: {status.counter}")
        print(f"   Max temp: {status.max_temp}")
    
    # Test 3: Augmenter le compteur
    print("\n3. Envoi T=6 C (Continue incident)")
    obj3 = Dht11.objects.create(temp=6, hum=50)
    status = Incident.objects.filter(is_open=True).first()
    print(f"   Incident ouvert: {bool(status)}")
    if status:
        print(f"   Compteur: {status.counter}")
        print(f"   Max temp: {status.max_temp}")
    
    # Test 4: Retour a la normale
    print("\n4. Envoi T=20 C (OK - fermeture incident)")
    obj4 = Dht11.objects.create(temp=20, hum=50)
    status = Incident.objects.filter(is_open=True).first()
    status_closed = Incident.objects.filter(is_open=False).first()
    print(f"   Incident ouvert: {bool(status)}")
    print(f"   Incident ferme: {bool(status_closed)}")
    if status_closed:
        print(f"   Compteur final: {status_closed.counter}")
    
    print("\n" + "="*60)
    print("TEST TERMINE")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_incident_flow()
