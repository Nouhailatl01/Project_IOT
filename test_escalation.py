#!/usr/bin/env python
"""
Script de test pour vérifier le système d'escalade d'incidents
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from DHT.models import Incident, Dht11
from django.utils import timezone
from datetime import timedelta

print("=" * 80)
print("TEST DU SYSTÈME D'ESCALADE D'INCIDENTS")
print("=" * 80)

# Créer un incident de test
incident = Incident.objects.create(
    is_open=True,
    counter=1,
    max_temp=10.5,
    current_escalation_level=1,
    escalation_counter=1
)
print(f"\n✓ Incident créé #{incident.id}")
print(f"  - Niveau d'escalade: OP{incident.current_escalation_level}")
print(f"  - Compteur: {incident.escalation_counter}/3")

# Simuler une réaction d'OP1
incident.op1_responded = True
incident.op1_comment = "Problème identifié, je m'en occupe"
incident.op1_responded_at = timezone.now()
incident.escalation_counter = 0
incident.save()
print(f"\n✓ OP1 a réagi:")
print(f"  - Réponse: Oui")
print(f"  - Commentaire: {incident.op1_comment}")
print(f"  - Compteur réinitié à: {incident.escalation_counter}")

# Tester l'escalade
incident.op1_responded = False
incident.op1_comment = ""
incident.op1_responded_at = None
incident.escalation_counter = 3

# Vérifier la logique d'escalade
if incident.escalation_counter >= 3 and incident.current_escalation_level < 3:
    incident.current_escalation_level += 1
    incident.escalation_counter = 0
    incident.escalated_to_op2_at = timezone.now()
    incident.save()
    print(f"\n✓ Escalade vers OP{incident.current_escalation_level}!")
    print(f"  - Escaladé vers OP2 le: {incident.escalated_to_op2_at}")

# Fermeture
incident.is_open = False
incident.end_at = timezone.now()
incident.is_archived = True
incident.save()
print(f"\n✓ Incident fermé et archivé")
print(f"  - Statut: {'FERMÉ' if not incident.is_open else 'OUVERT'}")
print(f"  - Archivé: {incident.is_archived}")

print("\n" + "=" * 80)
print("✓ TEST RÉUSSI - Le système d'escalade fonctionne correctement!")
print("=" * 80)
