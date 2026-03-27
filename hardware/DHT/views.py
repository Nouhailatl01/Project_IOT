# DHT/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Dht11, Incident, Operateur

# --- AUTHENTIFICATION ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_operator')
    
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Vérifier que c'est un opérateur
            if hasattr(user, 'operateur') and user.operateur.is_active:
                login(request, user)
                return redirect('dashboard_operator')
            else:
                error_message = "Vous n'avez pas accès à ce système."
        else:
            error_message = "Identifiant ou mot de passe incorrect."
    
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_operator(request):
    # Vérifier que l'utilisateur est un opérateur
    if not hasattr(request.user, 'operateur'):
        return redirect('login')
    
    operator = request.user.operateur
    return render(request, 'dashboard_operator.html', {
        'operator': operator,
        'operator_level': operator.level,
        'operator_name': operator.get_level_display()
    })

# --- DASHBOARD PUBLIC ---
def dashboard(request):
    # Rediriger vers login
    if request.user.is_authenticated:
        return redirect('dashboard_operator')
    return redirect('login')

def latest_json(request):
    # On trie par ID de manière décroissante pour obtenir le TOUT DERNIER enregistrement posté
    last = Dht11.objects.order_by('-id').first() 
    
    if not last:
        return JsonResponse({
            "temperature": 0,
            "humidity": 0,
            "timestamp": None
        })
    
    return JsonResponse({
        "temperature": last.temp,
        "humidity":    last.hum,
        "timestamp":   last.dt.isoformat()
    })

# --- LES DEUX FONCTIONS MANQUANTES ---
def graph_temp(request):
    return render(request, "graph_temp.html")

def graph_hum(request):
    return render(request, "graph_hum.html")

# --- ARCHIVES ET DETAILS ---
def incident_archive(request):
    from django.core.serializers.json import DjangoJSONEncoder
    import json
    
    # Trier: d'abord les ouverts (par start_at DESC), puis les fermés (par end_at DESC)
    incidents = Incident.objects.all().order_by("-is_open", "-end_at", "-start_at")
    
    # Convertir en JSON avec timestamps au format ISO
    incidents_data = []
    for inc in incidents:
        incidents_data.append({
            'id': inc.id,
            'start_at': inc.start_at.isoformat(),
            'end_at': inc.end_at.isoformat() if inc.end_at else None,
            'is_open': inc.is_open,
            'escalation_level': inc.escalation_level,
            'status': inc.status,
            'max_temp': float(inc.max_temp),
            'is_product_lost': inc.is_product_lost,
        })
    
    return render(request, "incident_archive.html", {
        "incidents": incidents,
        "incidents_data": json.dumps(incidents_data)
    })

def incident_detail(request, pk):
    import json
    incident = get_object_or_404(Incident, pk=pk)
    
    return render(request, "incident_detail.html", {
        "incident": incident
    })