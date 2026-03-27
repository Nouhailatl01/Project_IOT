#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

from django.contrib.auth.models import User
from DHT.models import Operateur

# Donnees des operateurs
operateurs_data = [
    {
        'username': 'op1',
        'full_name': 'Jean Dupont',
        'email': 'jean.dupont@company.com',
        'phone': '+33612345678',
        'level': 1
    },
    {
        'username': 'op2',
        'full_name': 'Marie Martin',
        'email': 'marie.martin@company.com',
        'phone': '+33623456789',
        'level': 2
    },
    {
        'username': 'op3',
        'full_name': 'Pierre Dubois',
        'email': 'pierre.dubois@company.com',
        'phone': '+33634567890',
        'level': 3
    }
]

for data in operateurs_data:
    username = data['username']
    password = 'password'
    
    # Creer ou mettre a jour l'utilisateur
    user, user_created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': data['full_name'].split()[0],
            'last_name': ' '.join(data['full_name'].split()[1:]),
            'email': data['email']
        }
    )
    
    if user_created:
        user.set_password(password)
        user.save()
        print("User {} created".format(username))
    else:
        user.first_name = data['full_name'].split()[0]
        user.last_name = ' '.join(data['full_name'].split()[1:])
        user.email = data['email']
        user.save()
        print("User {} updated".format(username))
    
    # Creer ou mettre a jour le profil operateur
    operateur, op_created = Operateur.objects.get_or_create(
        user=user,
        defaults={
            'level': data['level'],
            'full_name': data['full_name'],
            'email': data['email'],
            'phone': data['phone'],
            'is_active': True
        }
    )
    
    if op_created:
        print("Operateur {} profile created for {}".format(data['level'], username))
    else:
        operateur.full_name = data['full_name']
        operateur.email = data['email']
        operateur.phone = data['phone']
        operateur.is_active = True
        operateur.save()
        print("Operateur {} profile updated for {}".format(data['level'], username))

print("\nAll operator accounts are ready!")
print("\nTest accounts:")
for data in operateurs_data:
    print("  - {} / password (Operator {})".format(data['username'], data['level']))
