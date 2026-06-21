# Image de base : Python 3.12 en variante "slim" = légère, donc moins de
# paquets installés, donc moins de surface d'attaque (bon réflexe sécurité).
FROM python:3.12-slim

# PYTHONDONTWRITEBYTECODE : pas de fichiers .pyc inutiles dans le conteneur.
# PYTHONUNBUFFERED : les logs sortent en temps réel (sinon ils sont bufferisés).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dossier de travail à l'intérieur du conteneur. Les commandes suivantes
# s'exécutent depuis /app.
WORKDIR /app

# On copie D'ABORD uniquement requirements.txt, puis on installe.
# Astuce de cache : tant que ce fichier ne change pas, Docker réutilise la
# couche d'installation des dépendances et ne la rejoue pas -> builds rapides.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ENSUITE le code applicatif. Comme il change souvent, on le met après les
# dépendances pour ne pas invalider leur cache à chaque modif de code.
COPY main.py .

# On crée un utilisateur non-root et on bascule dessus. Si l'app est piratée,
# l'attaquant n'a PAS les droits root dans le conteneur. Pilier DevSecOps :
# un conteneur ne doit jamais tourner en root sans raison.
RUN useradd --create-home --uid 10001 appuser
USER appuser

# Documente le port sur lequel l'app écoute (purement informatif).
EXPOSE 8000

# Commande lancée au démarrage du conteneur. uvicorn = serveur ASGI qui sert
# l'objet 'app' du fichier main.py. host 0.0.0.0 = écoute sur toutes les
# interfaces DU CONTENEUR (indispensable pour que le proxy l'atteigne).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
