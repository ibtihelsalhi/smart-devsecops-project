    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    # On copie le modèle, le code et le template HTML
    COPY anomaly_model.joblib .
    COPY ia_service.py .
    COPY templates/ templates/
    EXPOSE 5001
    CMD ["python", "ia_service.py"]