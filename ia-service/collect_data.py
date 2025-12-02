import time
import pandas as pd
from prometheus_api_client import PrometheusConnect

# --- CONFIGURATION ---
PROMETHEUS_URL = "http://localhost:9090"
COLLECTION_DURATION = 300  # Durée de collecte en secondes (5 min)
SCRAPE_INTERVAL = 15        # Fréquence de collecte en secondes

print("--- Script de Collecte de Données Normales ---")
print("Assurez-vous que le tunnel Prometheus est ouvert :")
print("kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus-0 9090:9090\n")

# --- Connexion à Prometheus ---
try:
    print(f"Connexion à Prometheus sur {PROMETHEUS_URL}...")
    prom = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)
except Exception as e:
    print("Erreur de connexion ! Assurez-vous que le tunnel port-forward est actif.")
    print(f"Détail de l'erreur : {e}")
    exit()

print("Connexion réussie. Début de la collecte...\n")

data = []
start_time = time.time()

while time.time() - start_time < COLLECTION_DURATION:
    try:
        # Collecte des métriques
        cpu_usage = prom.custom_query(
            query='sum(rate(container_cpu_usage_seconds_total{namespace="banking-app"}[1m]))'
        )
        mem_usage = prom.custom_query(
            query='sum(container_memory_usage_bytes{namespace="banking-app"})'
        )
        net_rx = prom.custom_query(
            query='sum(rate(container_network_receive_bytes_total{namespace="banking-app"}[1m]))'
        )
        net_tx = prom.custom_query(
            query='sum(rate(container_network_transmit_bytes_total{namespace="banking-app"}[1m]))'
        )

        # Conversion sécurisée en float
        cpu = float(cpu_usage[0]['value'][1]) if cpu_usage else 0
        mem = float(mem_usage[0]['value'][1]) if mem_usage else 0
        rx = float(net_rx[0]['value'][1]) if net_rx else 0
        tx = float(net_tx[0]['value'][1]) if net_tx else 0

        timestamp = time.time()
        data.append([timestamp, cpu, mem, rx, tx])

        print(f"Collecté: CPU={cpu:.4f}, Mem={mem/1e6:.2f}MB, RX={rx:.2f}, TX={tx:.2f}")

    except Exception as e:
        print(f"Erreur pendant la collecte : {e}")

    time.sleep(SCRAPE_INTERVAL)

print("\nCollecte terminée.")

# Sauvegarde des données dans un fichier CSV
df = pd.DataFrame(data, columns=['timestamp', 'cpu_usage', 'mem_usage', 'net_rx', 'net_tx'])
df.to_csv('normal_traffic.csv', index=False)
print("Données sauvegardées dans 'normal_traffic.csv'.")
