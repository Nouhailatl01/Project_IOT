# 🗺️ MAPPING COMPLET DES URLs

## 📍 ALL ENDPOINTS

### 🔐 AUTHENTIFICATION

| Méthode | URL | Nom | Classe/View | Login | Description |
|---------|-----|-----|-------------|-------|-------------|
| GET/POST | `/login/` | `login` | `views.login_view` | ❌ | Écran connexion opérateur |
| GET | `/logout/` | `logout` | `views.logout_view` | ✅ | Déconnexion |

---

### 👥 DASHBOARDS

| Méthode | URL | Nom | Classe/View | Login | Description |
|---------|-----|-----|-------------|-------|-------------|
| GET | `/` | `dashboard` | `views.dashboard` | ❌ | Dashboard public (mesures temps réel) |
| GET | `/dashboard/` | `dashboard_operator` | `views.dashboard_operator` | ✅ | Dashboard opérateur (incidents + API test) |

---

### 📊 MESURES (DHT)

| Méthode | URL | Nom | Classe/View | Description |
|---------|-----|-----|-------------|-------------|
| GET | `/api/` | `json` | `api.DList.as_view()` | Lister toutes les mesures |
| POST | `/api/post` | `json_post` | `api.Dhtviews.as_view()` | Créer nouvelle mesure |
| GET | `/latest/` | `latest_json` | `views.latest_json` | Dernière mesure (JSON) |

---

### 📈 GRAPHES

| Méthode | URL | Nom | Classe/View | Description |
|---------|-----|-----|-------------|-------------|
| GET | `/graph_temp/` | `graph_temp` | `views.graph_temp` | Graphe température |
| GET | `/graph_hum/` | `graph_hum` | `views.graph_hum` | Graphe humidité |

---

### ⚠️ INCIDENTS (Gestion)

| Méthode | URL | Nom | Classe/View | Description |
|---------|-----|-----|-------------|-------------|
| GET | `/incident/status/` | `incident_status` | `api.IncidentStatus.as_view()` | État incident actuel |
| POST | `/incident/update/` | `incident_update` | `api.IncidentUpdateOperator.as_view()` | Valider opérateur (ACK + commentaire) |

---

### 📋 INCIDENTS (Archive & Détails)

| Méthode | URL | Nom | Classe/View | Description |
|---------|-----|-----|-------------|-------------|
| GET | `/incident/archive/` | `incident_archive` | `views.incident_archive` | Archive incidents fermés |
| GET | `/incident/<id>/` | `incident_detail` | `views.incident_detail` | Détails incident complet |

---

## 📡 DÉTAIL PAR ENDPOINT

### 1. Authentication

#### `GET/POST /login/`
```
Type: public
Render: login.html
POST params: username, password
Redirect: /dashboard/ si succès
Error: error_message dans context
```

#### `GET /logout/`
```
Type: public
Action: Django logout()
Redirect: /login/
```

---

### 2. Public Dashboards

#### `GET /`
```
Type: public
Render: dashboard.html
Context: 
  - Latest measures
  - Incident status
```

#### `GET /dashboard/`
```
Type: private (@login_required)
Render: dashboard_operator.html
Context:
  - operator (Operateur object)
  - operator_level (int: 1, 2, 3)
  - operator_name (str)
Check: hasattr(user, 'operateur')
```

---

### 3. API Endpoints

#### `GET /api/`
```
Type: API
Response: JSON Array
Fields: id, temp, hum, dt
Limit: All records
```

#### `POST /api/post`
```
Type: API
Input: { "temp": float, "hum": float }
Output: { "id": int, "temp": float, "hum": float, "dt": str }
Side-effect: Create/update Incident
Logic: T<2 or T>8 → incident
```

#### `GET /latest/`
```
Type: API
Response: JSON
Fields: temperature, humidity, timestamp
Order: DESC by id
Limit: 1
```

---

### 4. Graphs

#### `GET /graph_temp/`
```
Type: public
Render: graph_temp.html
Data: All Dht11.temp values
```

#### `GET /graph_hum/`
```
Type: public
Render: graph_hum.html
Data: All Dht11.hum values
```

---

### 5. Incident Management

#### `GET /incident/status/`
```
Type: API
Response: JSON
Fields: 
  {
    "id": int,
    "is_open": bool,
    "counter": int,
    "max_temp": float,
    "start_at": str,
    "end_at": str,
    "op1_ack": bool,
    "op1_comment": str,
    "op1_saved_at": str,
    "op2_ack": bool,
    "op2_comment": str,
    "op2_saved_at": str,
    "op3_ack": bool,
    "op3_comment": str,
    "op3_saved_at": str
  }
OR if no open incident:
  {
    "is_open": false,
    "counter": 0
  }
```

#### `POST /incident/update/`
```
Type: API
Input: {
  "op": int (1, 2, 3),
  "ack": bool,
  "comment": str
}
Output: Updated Incident (full JSON)
Side-effect: 
  - Set op{N}_ack
  - Set op{N}_comment
  - Set op{N}_saved_at = now()
```

---

### 6. Archive & Details

#### `GET /incident/archive/`
```
Type: public
Render: incident_archive.html
Filter: is_open=False
Order: -end_at
Context:
  - incidents: QuerySet[Incident]
  - total_alerts: int (calculated)
  - max_temp: float (calculated)
```

#### `GET /incident/<id>/`
```
Type: public
Render: incident_detail.html
Model: Incident
Context:
  - incident: Incident object
Display logic:
  - Op1 if counter >= 1
  - Op2 if counter >= 4
  - Op3 if counter >= 7
```

---

## 🔗 URL PATTERNS (Django)

### `DHT/urls.py`

```python
urlpatterns = [
    # Auth
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Dashboards
    path("dashboard/", views.dashboard_operator, name="dashboard_operator"),
    path("", views.dashboard, name="dashboard"),
    
    # API
    path("api/", api.DList.as_view(), name="json"),
    path("api/post", api.Dhtviews.as_view(), name='json_post'),
    path("latest/", views.latest_json, name="latest_json"),
    
    # Graphs
    path("graph_temp/", views.graph_temp, name="graph_temp"),
    path("graph_hum/", views.graph_hum, name="graph_hum"),
    
    # Incidents
    path("incident/status/", api.IncidentStatus.as_view(), name="incident_status"),
    path("incident/update/", api.IncidentUpdateOperator.as_view(), name="incident_update"),
    path("incident/archive/", views.incident_archive, name="incident_archive"),
    path("incident/<int:pk>/", views.incident_detail, name="incident_detail"),
]
```

---

## 🏗️ STRUCTURE DE RÉPONSE

### Success Response Format
```json
{
  "id": 123,
  "field1": "value1",
  "field2": "value2",
  "timestamp": "2025-12-31T14:52:00Z"
}
```

### Error Response Format
```json
{
  "error": "Error message",
  "status": 400
}
```

### Paginated Response Format
```json
{
  "count": 100,
  "next": "http://localhost/api/?page=2",
  "previous": null,
  "results": [
    { "id": 1, ... },
    { "id": 2, ... }
  ]
}
```

---

## 🔐 AUTHENTICATION REQUIRED

**Protected URLs** (require login):
- `/dashboard/` - GET
- `/incident/update/` - POST

**Public URLs** (no login needed):
- `/` - GET
- `/login/` - GET, POST
- `/logout/` - GET
- `/api/` - GET
- `/api/post` - POST
- `/latest/` - GET
- `/graph_temp/` - GET
- `/graph_hum/` - GET
- `/incident/status/` - GET
- `/incident/archive/` - GET
- `/incident/<id>/` - GET

---

## 💾 REQUEST/RESPONSE FORMATS

### HTML Forms
```
Content-Type: application/x-www-form-urlencoded
OR multipart/form-data
```

### JSON APIs
```
Content-Type: application/json
Accept: application/json
```

### Cookies
```
CSRF Token: required for POST
Session Cookie: for auth
```

---

## 🌐 EXEMPLE COMPLET

### 1. Login
```bash
POST /login/
Content-Type: application/x-www-form-urlencoded

username=op1&password=password

→ Redirect: /dashboard/
→ Set: SessionCookie
```

### 2. Dashboard
```bash
GET /dashboard/
Cookie: sessionid=...

→ Render: dashboard_operator.html
→ Context: operator, operator_name, etc.
```

### 3. Envoyer mesure
```bash
POST /api/post
Content-Type: application/json
X-CSRFToken: ...

{"temp": 15.5, "hum": 65.0}

→ 201 Created
→ Response: {id: 42, temp: 15.5, hum: 65.0, dt: "..."}
→ Side-effect: Incident created if T<2 or T>8
```

### 4. Vérifier état
```bash
GET /incident/status/

→ 200 OK
→ Response: {id: 1, is_open: true, counter: 1, ...}
```

### 5. Valider
```bash
POST /incident/update/
Content-Type: application/json
X-CSRFToken: ...

{"op": 1, "ack": true, "comment": "Acknowledged"}

→ 200 OK
→ Response: {id: 1, op1_ack: true, op1_comment: "...", ...}
```

### 6. Archive
```bash
GET /incident/archive/

→ 200 OK
→ Render: incident_archive.html
→ Context: incidents (closed list)
```

### 7. Détails
```bash
GET /incident/1/

→ 200 OK
→ Render: incident_detail.html
→ Context: incident (with all fields)
```

### 8. Logout
```bash
GET /logout/

→ Redirect: /login/
→ Clear: SessionCookie
```

---

**RÉFÉRENCE COMPLÈTE**
Mise à jour: 31/12/2025
Version: 1.0
