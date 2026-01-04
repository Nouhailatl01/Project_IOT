#!/usr/bin/env python
"""Debug: Vérifier l'état de la base de données"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Dht11, Incident

print("\n" + "="*70)
print("📊 ÉTAT DE LA BASE DE DONNÉES")
print("="*70)

# Dernières lectures DHT11
print("\n🌡️ DERNIÈRES LECTURES DHT11:")
for dht in Dht11.objects.all().order_by('-dt')[:5]:
    print(f"  ID={dht.id}: {dht.temp}°C, {dht.hum}%, {dht.dt}")

# Incidents ouverts
print("\n⚠️ INCIDENTS OUVERTS:")
open_incidents = Incident.objects.filter(is_open=True)
if open_incidents.exists():
    for inc in open_incidents:
        print(f"  ID={inc.id}: counter={inc.counter}, max_temp={inc.max_temp}, started={inc.start_at}")
else:
    print("  Aucun incident ouvert")

# Incidents fermés (derniers)
print("\n✅ DERNIERS INCIDENTS FERMÉS:")
closed_incidents = Incident.objects.filter(is_open=False).order_by('-end_at')[:3]
if closed_incidents.exists():
    for inc in closed_incidents:
        print(f"  ID={inc.id}: counter={inc.counter}, ended={inc.end_at}")
else:
    print("  Aucun incident fermé")

# Total
print(f"\n📈 STATISTIQUES:")
print(f"  Total DHT11: {Dht11.objects.count()}")
print(f"  Incidents ouverts: {Incident.objects.filter(is_open=True).count()}")
print(f"  Incidents fermés: {Incident.objects.filter(is_open=False).count()}")
print("="*70 + "\n")
