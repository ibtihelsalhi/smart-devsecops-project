# Utiliser une image de base Python 3.11 slim
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Créer un utilisateur non-privilégié et un groupe
RUN groupadd --gid 1001 appuser && \
    useradd --uid 1001 --gid 1001 -ms /bin/bash appuser

# Copier les dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Changer le propriétaire des fichiers pour notre nouvel utilisateur
RUN chown -R appuser:appuser /app

# Passer à l'utilisateur non-privilégié
USER appuser

# Ajouter une vérification de santé (HEALTHCHECK)
# Elle vérifie si l'application répond bien sur le port 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/login || exit 1

# Commande de démarrage
CMD ["python", "app.py"]