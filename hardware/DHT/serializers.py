from rest_framework import serializers
from .models import Dht11, Incident

class Dht11Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dht11
        fields = ["id", "temp", "hum", "dt"]
    
    def create(self, validated_data):
        """Override create pour ajouter du logging"""
        print(f"\n🔍 Dht11Serializer.create() appelé")
        print(f"   Données validées: {validated_data}")
        instance = super().create(validated_data)
        print(f"   Objet créé: ID={instance.id}, temp={instance.temp}, hum={instance.hum}")
        return instance

class IncidentSerializer(serializers.ModelSerializer):
    escalation_operators = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    is_resolved = serializers.SerializerMethodField()
    
    class Meta:
        model = Incident
        fields = [
            "id", "start_at", "end_at", "is_open", "status",
            "escalation_level", "escalation_operators",
            "max_temp", "min_temp", "max_hum", "min_hum",
            "op1_responded", "op1_comment", "op1_responded_at",
            "op2_responded", "op2_comment", "op2_responded_at",
            "op3_responded", "op3_comment", "op3_responded_at",
            "escalation_history", "is_product_lost",
            "duration", "is_resolved"
        ]
    
    def get_escalation_operators(self, obj):
        """Retourner la liste des opérateurs pour le niveau d'escalade courant"""
        return obj.get_escalation_operators()
    
    def get_duration(self, obj):
        """Retourner la durée de l'incident en secondes"""
        if obj.end_at:
            return (obj.end_at - obj.start_at).total_seconds()
        return None
    
    def get_is_resolved(self, obj):
        """Vérifier si incident est résolu"""
        return obj.is_resolved()
