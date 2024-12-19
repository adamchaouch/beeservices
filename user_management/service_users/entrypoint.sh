#!/bin/bash
set -e

# Initialiser Alembic si le dossier n'existe pas
if [ ! -d /app/app/db/alembic ]; then
    echo "Initialisation d'Alembic..."
    alembic init app/db/alembic
fi

# Générer la migration initiale si elle n'existe pas
if [ ! -d /app/app/db/alembic/versions ] || [ -z "$(ls -A /app/app/db/alembic/versions/*.py 2>/dev/null)" ]; then
    echo "Génération de la migration initiale..."
    alembic revision --autogenerate -m "Initial migration"
fi

# Appliquer les migrations
echo "Application des migrations..."
alembic upgrade head

# Démarrer l'application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
