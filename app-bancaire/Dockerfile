# Étape 1: Choisir notre point de départ
# On utilise une image officielle de Python, version 3.9, optimisée (slim).
FROM python:3.11-slim

# Étape 2: Définir l'espace de travail à l'intérieur de la "boîte"
# Toutes les commandes suivantes se dérouleront dans le dossier /app.
WORKDIR /app

# Étape 3: Installer les dépendances (la partie intelligente)
# On copie d'abord SEULEMENT le fichier requirements.txt.
COPY requirements.txt .
# On installe les bibliothèques listées. Si ce fichier ne change pas,
# Docker réutilisera le cache, ce qui rendra les builds futurs beaucoup plus rapides.
RUN pip install --no-cache-dir -r requirements.txt

# Étape 4: Copier le reste de notre application
# Maintenant, on copie tout le reste (app.py, templates/, static/).
COPY . .

# Étape 5: Définir la commande de démarrage
# C'est la commande qui sera exécutée quand on lancera la "boîte".
CMD ["python", "app.py"]