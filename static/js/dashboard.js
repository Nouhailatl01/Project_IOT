const MIN_OK = 2;
const MAX_OK = 8;
const KEY_STATE = "dht_incident_state_v5";

let state = {
  lastTimestamp: null,
  lastIncidentId: null,
  counter: 0,
};

// Sécurité pour éviter l'erreur "properties of null"
function $(id) {
    const el = document.getElementById(id);
    return el; 
}

function loadState() {
  try {
    const s = localStorage.getItem(KEY_STATE);
    if (s) state = { ...state, ...JSON.parse(s) };
  } catch (e) {
    console.error("Error loading state:", e);
  }
}

function saveState() {
  localStorage.setItem(KEY_STATE, JSON.stringify(state));
}

function formatAge(seconds) {
  const s = Math.max(0, seconds);
  if (s > 86400) return Math.floor(s/86400) + "j";
  if (s > 3600) return Math.floor(s/3600) + "h";
  if (s > 60) return Math.floor(s/60) + "min";
  return s + "s";
}

async function fetchIncidentStatus() {
  const res = await fetch("/incident/status/");
  if (!res.ok) throw new Error("Erreur incident status");
  return await res.json();
}

function setIncidentUI(isIncident) {
  if (!$("incident-badge")) return;
  
  $("incident-counter").textContent = state.alertCounter;
  
  if (!isIncident) {
    $("incident-badge").textContent = "OK";
    $("incident-badge").className = "badge ok";
    $("incident-status").textContent = "Pas d’incident";
    $("op1").classList.add("hidden");
    $("op2").classList.add("hidden");
    $("op3").classList.add("hidden");
  } else {
    $("incident-badge").textContent = "ALERTE";
    $("incident-badge").className = "badge alert";
    const counter = incident.counter || 0;
    
    // Afficher les opérateurs selon le compteur
    let operators = 'OP1';
    if (counter >= 4) operators += ' + OP2';
    if (counter >= 7) operators += ' + OP3';
    $("incident-status").textContent = `Alertés: ${operators}`;
    
    // Afficher les éléments
    if ($("op1")) $("op1").classList.remove("hidden");
    if (counter >= 4 && $("op2")) $("op2").classList.remove("hidden");
    if (counter >= 7 && $("op3")) $("op3").classList.remove("hidden");
  }
  
  // Mise à jour du state local
  state.lastIncidentId = incident.id;
  state.counter = incident.counter || 0;
  saveState();
}

async function loadLatest() {
  try {
    const res = await fetch("/latest/");
    if (!res.ok) return;
    const data = await res.json();

    const t = Number(data.temperature);
    const h = Number(data.humidity);

    // Mise à jour de l'affichage
    if ($("temp")) $("temp").textContent = t.toFixed(1) + " °C";
    if ($("hum")) $("hum").textContent = h.toFixed(1) + " %";

    const date = new Date(data.timestamp);
    const diffSec = Math.round((Date.now() - date.getTime()) / 1000);
    if ($("temp-time")) $("temp-time").textContent = "il y a " + formatAge(diffSec);
    if ($("hum-time")) $("hum-time").textContent = "il y a " + formatAge(diffSec);

    // Récupérer le statut courant de l'incident
    const incident = await fetchIncidentStatus();
    setIncidentUI(incident);

  } catch (e) {
    console.error("Erreur de rafraîchissement:", e);
  }
}

// Démarrage propre
document.addEventListener("DOMContentLoaded", () => {
    loadState();
    loadLatest();
    setInterval(loadLatest, 5000);
});
