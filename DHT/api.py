from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import timedelta, datetime
import json

from .models import Dht11, Incident
from .serializers import Dht11Serializer, IncidentSerializer
from .mqtt_client import mqtt_client

MIN_OK = 2
MAX_OK = 8

class DList(generics.ListAPIView):
    queryset = Dht11.objects.all()
    serializer_class = Dht11Serializer
    
    def get_queryset(self):
        """Filtrer les données selon les paramètres start_date et end_date"""
        queryset = super().get_queryset()
        
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            try:
                # Format: "2025-01-04T10:30"
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                # Rendre conscient du fuseau horaire (si nécessaire)
                if start_datetime.tzinfo is None:
                    start_datetime = timezone.make_aware(start_datetime)
                queryset = queryset.filter(dt__gte=start_datetime)
            except (ValueError, AttributeError, TypeError) as e:
                pass
        
        if end_date:
            try:
                # Format: "2025-01-04T20:30"
                end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                # Rendre conscient du fuseau horaire (si nécessaire)
                if end_datetime.tzinfo is None:
                    end_datetime = timezone.make_aware(end_datetime)
                queryset = queryset.filter(dt__lte=end_datetime)
            except (ValueError, AttributeError, TypeError) as e:
                pass
        
        # Trier par date croissante
        queryset = queryset.order_by('dt')
        
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = Dht11Serializer

    def create(self, request, *args, **kwargs):
        """Override to return JSON response instead of default HTML error page"""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e), "detail": "Failed to process sensor data"}, status=400)

    def perform_create(self, serializer):
        """
        Créer l'objet Dht11. La logique d'incident est gérée par le signal post_save.
        """
        try:
            obj = serializer.save()
            # Le signal post_save gérera automatiquement la création/mise à jour d'incident
        except Exception as e:
            print(f"❌ Error in perform_create: {str(e)}")
            raise

# ---- API incident: état courant ----
from rest_framework.views import APIView

class IncidentStatus(APIView):
    def get(self, request):
        """Retourner l'incident ouvert actuel ou le dernier incident"""
        # Retourner l'incident ouvert
        incident = Incident.objects.filter(is_open=True, status='open').order_by("-start_at").first()
        if not incident:
            # Si pas d'incident ouvert, retourner le dernier incident (archivé)
            incident = Incident.objects.order_by("-end_at", "-start_at").first()
        
        if not incident:
            return Response({
                "is_open": False,
                "escalation_level": 0,
                "status": "no_incident"
            })
        
        return Response(IncidentSerializer(incident).data)

# ---- API incident: valider réaction opérateur (op1/op2/op3) ----
@method_decorator(csrf_exempt, name='dispatch')
class IncidentUpdateOperator(APIView):
    def post(self, request):
        """
        Mettre à jour la réaction d'un opérateur et gérer l'escalade.
        
        Logique d'escalade :
        - Incident 1-3: Alerter OP1
        - Incident 4-6: Alerter OP1 + OP2
        - Incident 7+: Alerter OP1 + OP2 + OP3
        
        - Si un opérateur réagit (responded=true + commentaire valide):
          → Archiver l'incident immédiatement
          → escalation_level revient à 0
          → status devient 'resolved'
        
        body:
        {
          "op": 1,
          "responded": true,
          "comment": "..."
        }
        """
        try:
            op = int(request.data.get("op", 1))
            responded = bool(request.data.get("responded", False))
            comment = request.data.get("comment", "").strip()
            
            print(f"\n🔴 API IncidentUpdateOperator reçu:")
            print(f"   op={op}, responded={responded}, comment_len={len(comment)}")
        except (ValueError, TypeError) as e:
            print(f"❌ Erreur parsing: {e}")
            return Response({"error": "Invalid input", "details": str(e)}, status=400)

        # Récupérer l'incident ouvert
        incident = Incident.objects.filter(is_open=True, status='open').order_by("-start_at").first()
        if not incident:
            print(f"❌ Aucun incident ouvert trouvé")
            return Response({"error": "no open incident"}, status=400)

        print(f"   Incident trouvé: #{incident.id}, escalation_level={incident.escalation_level}")

        now = timezone.now()
        
        # Vérifier si 10h ont passé sans aucune réaction
        time_limit = incident.start_at + timedelta(hours=10)
        if now > time_limit and not incident.op1_responded and not incident.op2_responded and not incident.op3_responded:
            incident.is_product_lost = True
            print(f"   ⚠️ PRODUIT PERDU: 10h sans réaction")

        try:
            # Enregistrer la réaction de l'opérateur
            if op == 1:
                incident.op1_responded = responded
                incident.op1_comment = comment
                incident.op1_responded_at = now if responded else None
            elif op == 2:
                incident.op2_responded = responded
                incident.op2_comment = comment
                incident.op2_responded_at = now if responded else None
            elif op == 3:
                incident.op3_responded = responded
                incident.op3_comment = comment
                incident.op3_responded_at = now if responded else None
            else:
                print(f"❌ Opérateur invalide: {op}")
                return Response({"error": "Invalid operator level"}, status=400)

            # LOGIQUE PRINCIPALE :
            # Si opérateur a réagi (responded=true) ET a écrit un commentaire valide
            # → ARCHIVER IMMÉDIATEMENT l'incident et réinitialiser
            if responded and len(comment) > 0:
                print(f"   ✅ INCIDENT RÉSOLU par Opérateur {op}")
                print(f"      Commentaire: '{comment[:50]}...'")
                
                # Archiver l'incident
                incident.is_open = False
                incident.status = 'resolved'
                incident.end_at = now
                incident.escalation_level = 0  # Réinitialiser le niveau d'escalade
                
                print(f"   📦 Incident archivé avec tous les détails")
            else:
                print(f"   ⚠️ Réaction incomplète (responded={responded}, comment_len={len(comment)})")
                print(f"      L'escalade continue au niveau {incident.escalation_level}")
            
            incident.save()
            print(f"   ✅ Incident sauvegardé: status={incident.status}, escalation_level={incident.escalation_level}")
            
            return Response(IncidentSerializer(incident).data)
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

# ---- API: Lister tous les incidents archivés ----
class IncidentArchiveList(generics.ListAPIView):
    """Retourner tous les incidents archivés avec leurs détails"""
    queryset = Incident.objects.filter(status__in=['resolved', 'archived']).order_by('-end_at')
    serializer_class = IncidentSerializer

# ---- API: Détails d'un incident archivé ----
class IncidentArchiveDetail(generics.RetrieveAPIView):
    """Retourner les détails complets d'un incident archivé"""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    lookup_field = 'id'

# ===== API MQTT =====

class MQTTStatusView(APIView):
    """Obtenir le statut de la connexion MQTT"""
    
    def get(self, request):
        return Response({
            'connected': mqtt_client.connected,
            'broker': mqtt_client.broker_address,
            'port': mqtt_client.broker_port,
            'client_id': mqtt_client.client_id,
            'topics': {
                'sensor_data': mqtt_client.topic_sensor_data,
                'incidents': mqtt_client.topic_incidents,
                'alerts': mqtt_client.topic_alerts,
                'status': mqtt_client.topic_status,
            }
        })


class MQTTPublishSensorView(APIView):
    """Publier des données de capteur via MQTT"""
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            data = request.data if hasattr(request, 'data') else json.loads(request.body)
            
            temp = data.get('temperature')
            hum = data.get('humidity')
            
            if temp is None or hum is None:
                return Response(
                    {'error': 'Les champs temperature et humidity sont requis'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not mqtt_client.connected:
                return Response(
                    {'error': 'Client MQTT non connecté'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            if mqtt_client.publish_sensor_data(float(temp), float(hum)):
                return Response({
                    'success': True,
                    'message': f'Données publiées: T={temp}°C, H={hum}%',
                    'temperature': temp,
                    'humidity': hum
                })
            else:
                return Response(
                    {'error': 'Erreur lors de la publication'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MQTTPublishIncidentView(APIView):
    """Publier un incident via MQTT"""
    
    @method_decorator(csrf_exempt)
    def post(self, request, incident_id):
        try:
            incident = Incident.objects.get(id=incident_id)
            
            if not mqtt_client.connected:
                return Response(
                    {'error': 'Client MQTT non connecté'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            if mqtt_client.publish_incident(incident):
                return Response({
                    'success': True,
                    'message': f'Incident {incident_id} publié via MQTT',
                    'incident_id': incident_id
                })
            else:
                return Response(
                    {'error': 'Erreur lors de la publication'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Incident.DoesNotExist:
            return Response(
                {'error': f'Incident {incident_id} non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MQTTConnectView(APIView):
    """Initier la connexion MQTT"""
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            data = request.data if hasattr(request, 'data') else json.loads(request.body)
            
            # Mettre à jour les paramètres
            if 'broker' in data:
                mqtt_client.broker_address = data['broker']
            if 'port' in data:
                mqtt_client.broker_port = data['port']
            if 'username' in data:
                mqtt_client.username = data['username']
            if 'password' in data:
                mqtt_client.password = data['password']
            
            # Se connecter
            if mqtt_client.setup():
                return Response({
                    'success': True,
                    'message': 'Connexion MQTT établie',
                    'broker': mqtt_client.broker_address,
                    'port': mqtt_client.broker_port
                })
            else:
                return Response(
                    {'error': 'Impossible de se connecter au broker MQTT'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MQTTDisconnectView(APIView):
    """Fermer la connexion MQTT"""
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            mqtt_client.disconnect()
            return Response({
                'success': True,
                'message': 'Déconnexion MQTT effectuée'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )