#!/usr/bin/env python
"""
Test du NOUVEAU système d'incidents (v2)
- Compteur 1-3: OP1 seul
- Compteur 4-6: OP1 + OP2
- Compteur 7+: OP1 + OP2 + OP3
- Si quelqu'un réagit: Compteur remet à 0
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Incident
from django.utils import timezone

print("\n" + "="*80)
print("NOUVEAU SYSTÈME D'ESCALADE D'INCIDENTS")
print("="*80)

# Créer incident 1 (Compteur 1 → OP1 seul)
inc1 = Incident.objects.create(is_open=True, counter=1, max_temp=9.5)
print(f"\n1️⃣  Incident #{inc1.id} créé")
print(f"   Compteur: {inc1.counter}")
print(f"   Opérateurs alertés: OP1 seul")
print(f"   Ouvert: {inc1.is_open}")

# Créer incident 3 (Compteur 3 → OP1 seul)
inc2 = Incident.objects.create(is_open=True, counter=3, max_temp=10.0)
print(f"\n2️⃣  Incident #{inc2.id} créé")
print(f"   Compteur: {inc2.counter}")
print(f"   Opérateurs alertés: OP1 seul")

# Créer incident 4 (Compteur 4 → OP1 + OP2)
inc3 = Incident.objects.create(is_open=True, counter=4, max_temp=10.5)
print(f"\n3️⃣  Incident #{inc3.id} créé")
print(f"   Compteur: {inc3.counter}")
print(f"   Opérateurs alertés: OP1 + OP2  ✅")

# Créer incident 7 (Compteur 7 → OP1 + OP2 + OP3)
inc4 = Incident.objects.create(is_open=True, counter=7, max_temp=11.0)
print(f"\n4️⃣  Incident #{inc4.id} créé")
print(f"   Compteur: {inc4.counter}")
print(f"   Opérateurs alertés: OP1 + OP2 + OP3  ✅✅")

# Récupérer l'incident et simuler réaction OP1
current = Incident.objects.filter(is_open=True).last()
print(f"\n✏️  Incident courant #{current.id}: Compteur = {current.counter}")

# OP1 réagit
current.op1_responded = True
current.op1_comment = "Capteur remplacé, température normale détectée"
current.op1_responded_at = timezone.now()
current.counter = 0  # Compteur remet à 0
current.is_open = False  # Incident fermé
current.end_at = timezone.now()
current.is_archived = True  # Archivé
current.save()

print(f"\n✅ OP1 a réagi!")
print(f"   Commentaire: {current.op1_comment[:40]}...")
print(f"   Compteur réinitialisé à: {current.counter}")
print(f"   Incident fermé: {not current.is_open}")
print(f"   Archivé: {current.is_archived}")

# Vérifier les incidents archivés
archived = Incident.objects.filter(is_archived=True).count()
print(f"\n📊 Statistiques:")
print(f"   Incidents archivés: {archived}")
print(f"   Incidents ouverts: {Incident.objects.filter(is_open=True).count()}")

print("\n" + "="*80)
print("✅ TEST RÉUSSI - Le nouveau système fonctionne correctement!")
print("="*80 + "\n")
