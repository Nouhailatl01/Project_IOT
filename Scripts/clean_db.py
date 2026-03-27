#!/usr/bin/env python
"""Nettoyer les incidents anciens"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Incident, Dht11

print("\n" + "="*70)
print("🧹 NETTOYAGE DE LA BASE DE DONNÉES")
print("="*70)

# Afficher l'état avant
print("\n📊 AVANT:")
print(f"  Dht11: {Dht11.objects.count()}")
print(f"  Incidents: {Incident.objects.count()}")

# Nettoyer
Dht11.objects.all().delete()
Incident.objects.all().delete()

# Afficher l'état après
print("\n📊 APRÈS:")
print(f"  Dht11: {Dht11.objects.count()}")
print(f"  Incidents: {Incident.objects.count()}")

print("\n✅ BASE DE DONNÉES NETTOYÉE")
print("="*70 + "\n")
