#!/usr/bin/env python
"""Créer les comptes de test pour les opérateurs"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from django.contrib.auth.models import User
from DHT.models import Operateur

print("\n" + "="*70)
print("🔐 CRÉATION DES COMPTES DE TEST")
print("="*70)

# Données des comptes de test
test_accounts = [
    {"username": "op1", "password": "password", "level": 1},
    {"username": "op2", "password": "password", "level": 2},
    {"username": "op3", "password": "password", "level": 3},
]

for account in test_accounts:
    username = account["username"]
    password = account["password"]
    level = account["level"]
    
    # Supprimer l'utilisateur s'il existe déjà
    User.objects.filter(username=username).delete()
    
    # Créer l'utilisateur
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=f"Opérateur",
        last_name=f"{level}",
        email=f"{username}@example.com"
    )
    
    # Créer l'opérateur associé
    op, created = Operateur.objects.get_or_create(
        user=user,
        defaults={
            'level': level,
            'is_active': True,
            'full_name': f"Opérateur {level}",
            'email': f"{username}@example.com"
        }
    )
    
    print(f"\n✅ {username.upper()}")
    print(f"   Utilisateur créé: {user.username}")
    print(f"   Mot de passe: {password}")
    print(f"   Email: {user.email}")
    print(f"   Niveau: {level}")

print("\n" + "="*70)
print("✅ TOUS LES COMPTES CRÉÉS AVEC SUCCÈS")
print("\n📝 Vous pouvez maintenant vous connecter avec:")
for account in test_accounts:
    print(f"   {account['username']} / {account['password']}")

print("="*70 + "\n")
