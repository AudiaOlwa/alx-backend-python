# Utiliser Python 3.10 (version légère)
FROM python:3.10-slim

# Installer les dépendances système nécessaires à mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Définir le dossier de travail
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Exposer le port utilisé par Django
EXPOSE 8000

# Commande de démarrage du serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
