from django.db import models
from django.contrib.auth.models import User

class Operateur(models.Model):
    """Modèle pour les opérateurs"""
    LEVEL_CHOICES = [
        (1, 'Opérateur 1'),
        (2, 'Opérateur 2'),
        (3, 'Opérateur 3'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operateur')
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_level_display()} - {self.user.username}"

class Dht11(models.Model):
    temp = models.FloatField(null=True, blank=True)
    hum = models.FloatField(null=True, blank=True)
    dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dt"]

    def __str__(self):
        return f"{self.dt} -> T={self.temp}°C, H={self.hum}%"

class Incident(models.Model):
    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('resolved', 'Résolu'),
        ('archived', 'Archivé'),
    ]
    
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    is_open = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    # Compteur d'escalade (1-7+)
    escalation_level = models.IntegerField(default=0)  # Niveau d'escalade: 0=fermé, 1-3=Op1, 4-6=Op1+Op2, 7+=Op1+Op2+Op3
    
    # Données des capteurs
    max_temp = models.FloatField(default=0)
    min_temp = models.FloatField(default=999)
    max_hum = models.FloatField(default=0)
    min_hum = models.FloatField(default=100)
    
    # Réactions opérateurs (True = a réagi avec commentaire)
    op1_responded = models.BooleanField(default=False)
    op2_responded = models.BooleanField(default=False)
    op3_responded = models.BooleanField(default=False)

    # Commentaires opérateurs
    op1_comment = models.TextField(blank=True, null=True)
    op2_comment = models.TextField(blank=True, null=True)
    op3_comment = models.TextField(blank=True, null=True)

    # Timestamps de réaction
    op1_responded_at = models.DateTimeField(null=True, blank=True)
    op2_responded_at = models.DateTimeField(null=True, blank=True)
    op3_responded_at = models.DateTimeField(null=True, blank=True)
    
    # Détails d'escalade archivés
    escalation_history = models.JSONField(default=dict, blank=True)  # Historique des escalades
    is_product_lost = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_at"]

    def __str__(self):
        return f"Incident #{self.id} (Level {self.escalation_level}) - {self.status}"
    
    def get_escalation_operators(self):
        """Retourner les opérateurs à alerter selon le niveau d'escalade"""
        if self.escalation_level <= 3:
            return [1]  # Opérateur 1 uniquement
        elif self.escalation_level <= 6:
            return [1, 2]  # Opérateurs 1 et 2
        else:
            return [1, 2, 3]  # Opérateurs 1, 2 et 3
    
    def is_resolved(self):
        """Vérifier si l'incident est résolu (quelqu'un a réagi)"""
        return self.op1_responded or self.op2_responded or self.op3_responded
