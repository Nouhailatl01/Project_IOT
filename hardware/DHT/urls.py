from django.urls import path
from . import views
from . import api

urlpatterns = [
    # Authentification
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_operator, name="dashboard_operator"),
    
    # Interface public (ancien dashboard)
    path("", views.dashboard, name="dashboard"),
    
    # API
    path("api/", api.DList.as_view(), name="json"),
    path("api/post", api.Dhtviews.as_view(), name='json_post'),
    path("latest/", views.latest_json, name="latest_json"),
    path("graph_temp/", views.graph_temp, name="graph_temp"),
    path("graph_hum/", views.graph_hum, name="graph_hum"),
    
    # API Incidents
    path("incident/status/", api.IncidentStatus.as_view(), name="incident_status"),
    path("incident/update/", api.IncidentUpdateOperator.as_view(), name="incident_update"),
    path("incident/archive/list/", api.IncidentArchiveList.as_view(), name="incident_archive_list"),
    path("incident/archive/<int:id>/", api.IncidentArchiveDetail.as_view(), name="incident_archive_detail"),
    
    # Vues HTML
    path("incident/archive/", views.incident_archive, name="incident_archive"),
    path("incident/<int:pk>/", views.incident_detail, name="incident_detail"),
    
    # API MQTT
    path("mqtt/status/", api.MQTTStatusView.as_view(), name="mqtt_status"),
    path("mqtt/publish/sensor/", api.MQTTPublishSensorView.as_view(), name="mqtt_publish_sensor"),
    path("mqtt/publish/incident/<int:incident_id>/", api.MQTTPublishIncidentView.as_view(), name="mqtt_publish_incident"),
    path("mqtt/connect/", api.MQTTConnectView.as_view(), name="mqtt_connect"),
    path("mqtt/disconnect/", api.MQTTDisconnectView.as_view(), name="mqtt_disconnect"),]