import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib  # Pour sauvegarder le modèle

print("--- Script d'Entraînement du Modèle ---")

# --- Charger les données ---
try:
    df = pd.read_csv('normal_traffic.csv')
    print("Données 'normal_traffic.csv' chargées.")
except FileNotFoundError:
    print("Erreur : Le fichier 'normal_traffic.csv' n'a pas été trouvé.")
    print("Veuillez d'abord lancer 'collect_data.py'.")
    exit()

# --- Sélectionner les caractéristiques (features) pour l'entraînement ---
features = ['cpu_usage', 'mem_usage', 'net_rx', 'net_tx']
X = df[features]

# --- Définir et entraîner le modèle Isolation Forest ---
# 'contamination' est le pourcentage approximatif d'anomalies attendues
# On met une très faible valeur car nos données d'entraînement sont "propres"
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
print("Entraînement du modèle Isolation Forest...")
model.fit(X)
print("Entraînement terminé.")

# --- Sauvegarder le modèle entraîné ---
joblib.dump(model, 'anomaly_model.joblib')
print("Modèle sauvegardé dans 'anomaly_model.joblib'.")
