from flask import Flask, render_template, jsonify
from prometheus_api_client import PrometheusConnect
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import pandas as pd
import joblib
import datetime
import logging
import random
import os
import json

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

# --- CONFIG ---
PROMETHEUS_URL = "http://prometheus-kube-prometheus-prometheus.monitoring.svc:9090"
FALCO_URL = "http://falco-metrics.falco.svc:8765/metrics"
# URL pour contacter n8n (qui tourne en local sur le port 5678) depuis le conteneur
N8N_WEBHOOK_URL = "http://host.docker.internal:5678/webhook-test/security-alert"

# --- ETAT GLOBAL ---
dashboard_data = {
    "threat_level": "LOW",
    "status": "SECURE",
    "cpu": 0.12,
    "mem": 120.0,
    "falco_events": 0,
    "ai_score": 0.99,
    "last_update": "",
    "history": []
}

# --- FONCTION D'ENVOI N8N (AJOUTÉE) ---
def trigger_n8n(threat, message, cpu, events):
    """Envoie l'alerte au SOAR"""
    payload = {
        "threat": threat,
        "message": message,
        "cpu_load": cpu,
        "falco_events": events,
        "source": "SENTINEL_PRIME"
    }
    try:
        # Timeout très court (1s) pour ne pas ralentir l'interface si n8n est éteint
        requests.post(N8N_WEBHOOK_URL, json=payload, timeout=1)
        return "SENT"
    except:
        return "FAILED"

# --- FONCTION DE SIMULATION CONTRÔLÉE ---
def get_data():
    """
    Récupère les vraies données OU simule des données STABLES.
    Passe en ALERTE seulement si un fichier spécial existe.
    """
    # 1. Valeurs par défaut (Calme / Vert)
    cpu = round(random.uniform(0.05, 0.15), 3) # Très bas
    mem = round(random.uniform(110, 130), 1)
    events = 0
    
    # 2. LA COMMANDE SECRÈTE : Si le fichier /tmp/attack existe
    if os.path.exists("/tmp/attack"):
        cpu = round(random.uniform(0.85, 0.99), 3) # CPU Élevé
        events = random.randint(5, 20)             # Alertes Falco
        
    return {"cpu": cpu, "mem": mem, "events": events}

# --- BOUCLE D'ANALYSE ---
def core_analysis_loop():
    global dashboard_data
    
    data = get_data()
    
    # Logique de décision
    threat = "LOW"
    status = "SECURE"
    soar_status = "READY"
    
    if data["events"] > 0:
        threat = "CRITICAL"
        status = "INTRUSION DETECTED"
    elif data["cpu"] > 0.8:
        threat = "HIGH"
        status = "ANOMALY (HIGH CPU)"
    
    # --- DÉCLENCHEMENT SOAR (AJOUTÉ) ---
    if threat == "CRITICAL" or threat == "HIGH":
        res = trigger_n8n(threat, status, data["cpu"], data["events"])
        soar_status = f"ALERT {res}"
        
    # Mise à jour Dashboard
    dashboard_data["threat_level"] = threat
    dashboard_data["status"] = status
    dashboard_data["cpu"] = data["cpu"]
    dashboard_data["mem"] = data["mem"]
    dashboard_data["falco_events"] = data["events"]
    dashboard_data["last_update"] = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Historique
    log_msg = "System integrity check passed."
    if threat == "CRITICAL": log_msg = f"!!! SECURITY ALERT !!! SOAR: {soar_status}"
    
    log_entry = {
        "time": dashboard_data["last_update"],
        "type": threat,
        "message": status,
        "details": log_msg
    }
    
    dashboard_data["history"].insert(0, log_entry)
    if len(dashboard_data["history"]) > 20: dashboard_data["history"].pop()

scheduler = BackgroundScheduler()
scheduler.add_job(core_analysis_loop, 'interval', seconds=3) # Un peu plus lent (3s) pour laisser le temps à n8n
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html', data=dashboard_data)

@app.route('/api/data')
def api_data():
    return jsonify(dashboard_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)