# ia-service/ia_service.py
from flask import Flask, request, jsonify
# import joblib  # On l'utilisera plus tard pour charger notre modèle entraîné

app = Flask(__name__)

# --- Placeholder pour notre modèle d'IA ---
# Dans la Phase 3, nous chargerons ici un vrai modèle entraîné.
# Pour l'instant, c'est une variable vide.
model = None
print("AI Service Started: Model not loaded yet.")
# -------------------------------------------

@app.route('/predict', methods=['POST'])
def predict():
    """
    Cet endpoint recevra des données (ex: métriques de Prometheus, logs de Loki)
    et utilisera le modèle d'IA pour retourner un score d'anomalie.
    """
    # 1. Récupérer les données envoyées à l'API
    data = request.json
    print(f"Received data for prediction: {data}")
    
    # 2. (Phase 3) Ici, on préparera les données pour le modèle.
    
    # 3. (Phase 3) Ici, on utilisera le modèle pour prédire.
    #    anomaly_score = model.predict(prepared_data)
    
    # 4. Pour l'instant, on retourne un score factice pour simuler le fonctionnement.
    simulated_score = -1 if data.get('failed_logins', 0) > 5 else 1
    
    print(f"Simulated anomaly score: {simulated_score}")
    
    # Un score de -1 signifie "anomalie", 1 signifie "normal" avec IsolationForest.
    return jsonify({"anomaly_score": simulated_score})

if __name__ == '__main__':
    # Dans un vrai déploiement, on utiliserait un serveur WSGI comme Gunicorn.
    # Pour le développement, c'est parfait.
    app.run(host='0.0.0.0', port=5001, debug=True)