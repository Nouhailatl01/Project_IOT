#!/usr/bin/env python
"""Test l'endpoint /incident/status/"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Incident
from DHT.serializers import IncidentSerializer

print("\n" + "="*70)
print("🔍 TEST ENDPOINT /incident/status/")
print("="*70)

# Récupérer l'incident ouvert
incident = Incident.objects.filter(is_open=True).order_by("-start_at").first()

if incident:
    print(f"\n✅ Incident trouvé: ID={incident.id}")
    print(f"   Counter: {incident.counter}")
    print(f"   Is Open: {incident.is_open}")
    print(f"   Max Temp: {incident.max_temp}")
    
    # Sérialiser
    serializer = IncidentSerializer(incident)
    data = serializer.data
    print(f"\n📋 Réponse sérialisée:")
    print(json.dumps(data, indent=2, default=str))
else:
    print("\n❌ Aucun incident ouvert")

print("\n" + "="*70 + "\n")
