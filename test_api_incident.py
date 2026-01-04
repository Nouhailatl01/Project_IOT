#!/usr/bin/env python
"""
Test API: Vérifier que l'API incident/status/ retourne les bonnes données
"""

import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Dht11, Incident
from DHT.serializers import IncidentSerializer
from rest_framework.test import APIRequestFactory
from DHT.api import IncidentStatus

def test_api_responses():
    """Test les réponses de l'API"""
    
    print("\n" + "="*60)
    print("TEST API: Vérifier les réponses incident/status/")
    print("="*60)
    
    # Nettoyer
    Incident.objects.all().delete()
    Dht11.objects.all().delete()
    
    # Test 1: Pas d'incident
    print("\n1️⃣  Pas d'incident")
    factory = APIRequestFactory()
    request = factory.get('/incident/status/')
    view = IncidentStatus.as_view()
    response = view(request)
    data = response.data
    print(f"   Réponse: {json.dumps(data, indent=2, default=str)}")
    assert not data.get('is_open'), "Devrait être False quand pas d'incident"
    print(f"   ✓ OK: is_open={data.get('is_open')}")
    
    # Test 2: Créer un incident
    print("\n2️⃣  Créer incident avec counter=1")
    incident = Incident.objects.create(is_open=True, counter=1, max_temp=0.5)
    
    request = factory.get('/incident/status/')
    response = view(request)
    data = response.data
    print(f"   Réponse: {json.dumps(data, indent=2, default=str)}")
    assert data.get('is_open') == True, "Devrait être True"
    assert data.get('counter') == 1, "Counter devrait être 1"
    print(f"   ✓ OK: is_open={data.get('is_open')}, counter={data.get('counter')}")
    
    # Test 3: Incrémenter à counter=5
    print("\n3️⃣  Incrémenter à counter=5")
    incident.counter = 5
    incident.max_temp = 1.5
    incident.save()
    
    request = factory.get('/incident/status/')
    response = view(request)
    data = response.data
    print(f"   Réponse: {json.dumps(data, indent=2, default=str)}")
    assert data.get('counter') == 5, "Counter devrait être 5"
    print(f"   ✓ OK: counter={data.get('counter')}")
    
    # Test 4: Archiver l'incident
    print("\n4️⃣  Archiver incident")
    incident.is_open = False
    incident.is_archived = True
    incident.save()
    
    request = factory.get('/incident/status/')
    response = view(request)
    data = response.data
    print(f"   Réponse: {json.dumps(data, indent=2, default=str)}")
    assert data.get('is_open') == False, "Devrait être False"
    assert data.get('is_archived') == True, "Devrait être archivé"
    print(f"   ✓ OK: is_open={data.get('is_open')}, is_archived={data.get('is_archived')}")
    
    # Test 5: Créer nouvel incident après archivage
    print("\n5️⃣  Créer nouvel incident après archivage")
    new_incident = Incident.objects.create(is_open=True, counter=1, max_temp=0.5)
    
    request = factory.get('/incident/status/')
    response = view(request)
    data = response.data
    print(f"   Réponse: {json.dumps(data, indent=2, default=str)}")
    assert data.get('id') == new_incident.id, "Devrait retourner le nouvel incident"
    assert data.get('counter') == 1, "Counter du nouvel incident devrait être 1"
    print(f"   ✓ OK: Nouvel incident, ID={data.get('id')}, counter={data.get('counter')}")
    
    print("\n" + "="*60)
    print("✅ TOUS LES TESTS API PASSÉS !")
    print("="*60)

if __name__ == "__main__":
    test_api_responses()
