# ia-service/evaluate_model.py
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

print("--- Script d'Évaluation du Modèle ---")

# --- 1. Chargement des données et du modèle ---
try:
    model = joblib.load('anomaly_model.joblib')
    df_normal = pd.read_csv('normal_traffic.csv')
    print("Modèle et données normales chargés.")
except FileNotFoundError:
    print("Erreur : Assurez-vous que 'anomaly_model.joblib' et 'normal_traffic.csv' existent.")
    exit()

# --- 2. Création de fausses anomalies ---
print("Création de données d'anomalies simulées...")
df_anomaly = df_normal.copy()

# On va créer 5 anomalies en modifiant drastiquement certaines valeurs
num_anomalies = 5
anomaly_indices = np.random.choice(df_anomaly.index, num_anomalies, replace=False)

# Augmenter massivement le CPU et la mémoire pour ces points
df_anomaly.loc[anomaly_indices, 'cpu_usage'] *= 10  # CPU x10
df_anomaly.loc[anomaly_indices, 'mem_usage'] *= 3   # Mémoire x3

# Créer les "vraies" étiquettes : 1 pour normal, -1 pour anomalie
y_true_normal = np.ones(len(df_normal))
y_true_anomaly = np.full(len(df_anomaly), 1)  # Commence avec tout à "normal"
y_true_anomaly[anomaly_indices] = -1          # Marque nos anomalies

# Combiner les données normales et celles avec anomalies
df_test = pd.concat([df_normal, df_anomaly])
y_true = np.concatenate([y_true_normal, y_true_anomaly])

# --- 3. Prédiction sur le jeu de test ---
print("Prédiction sur le jeu de données de test...")
features = ['cpu_usage', 'mem_usage', 'net_rx', 'net_tx']
X_test = df_test[features]
y_pred = model.predict(X_test)

# --- 4. Évaluation quantitative ---
print("\n--- Rapport de Classification ---")
print(classification_report(
    y_true,
    y_pred,
    target_names=['Anomalie (-1)', 'Normal (1)']
))

print("\n--- Matrice de Confusion ---")
cm = confusion_matrix(y_true, y_pred, labels=[-1, 1])

print("                 Prédit Anomalie | Prédit Normal")
print(f"Vraie Anomalie:        {cm[0][0]}         |       {cm[0][1]}")
print(f"Vrai Normal:           {cm[1][0]}         |       {cm[1][1]}")

# --- 5. Évaluation visuelle ---
print("\nGénération du graphique de la matrice de confusion...")

plt.figure(figsize=(8, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=['Anomalie', 'Normal'],
    yticklabels=['Anomalie', 'Normal']
)

plt.xlabel('Prédiction')
plt.ylabel('Vraie valeur')
plt.title("Matrice de Confusion du Modèle de Détection d'Anomalies")

# Sauvegarde du graphique dans un fichier
plt.savefig('confusion_matrix.png')
print("Graphique sauvegardé dans 'confusion_matrix.png'.")
plt.show()
