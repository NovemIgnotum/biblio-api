#!/bin/bash

# -------------------------------------------------------------------
# Script de démarrage pour l'application de bibliothèque
# Usage : ./start.sh [--build] [--logs] [--stop]
# -------------------------------------------------------------------

# Variables
COMPOSE_FILE="docker-compose.yml"
APP_NAME="biblio-api"
LOG_FILE="docker.log"
VENV_DIR="venv"

# Fonctions
show_help() {
  echo "Usage: $0 [OPTIONS]"
  echo
  echo "Options:"
  echo "  --build     Reconstruit les images Docker avant démarrage"
  echo "  --logs      Affiche les logs en temps réel"
  echo "  --stop      Arrête les conteneurs et nettoie"
  echo "  --help      Affiche cette aide"
  echo
  echo "Exemples:"
  echo "  ./start.sh --build --logs  # Fresh install avec affichage des logs"
  echo "  ./start.sh --stop          # Nettoyage complète"
}

check_docker() {
  if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker avant de continuer."
    exit 1
  fi

  if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose V2 n'est pas installé. Veuillez mettre à jour Docker."
    exit 1
  fi
}

check_venv() {
  if [ ! -d "$VENV_DIR" ]; then
    echo "❌ L'environnement virtuel '$VENV_DIR' n'existe pas. Veuillez le créer avec :"
    echo "  python -m venv venv"
    exit 1
  fi
  echo "✅ L'environnement virtuel '$VENV_DIR' est prêt."
}

start_services() {
  echo "🔄 Démarrage des services..."
  
  if [ "$1" == "--build" ]; then
    echo "🛠️  Reconstruction des images Docker..."
    docker compose -f "$COMPOSE_FILE" build --no-cache
  fi
  
  # Démarrage des services en arrière-plan
  docker compose -f "$COMPOSE_FILE" up -d

  # Vérification du statut de Docker et affichage des logs si nécessaire
  if [ "$2" == "--logs" ]; then
    echo "📜 Affichage des logs (CTRL+C pour quitter)..."
    docker compose -f "$COMPOSE_FILE" logs -f
  else
    echo "✅ Les docker des bases de données sont bien lancés :"
    echo " - pgAdmin:    http://localhost:5050"
    echo " - Mongo-UI:   http://localhost:8081"
    echo
    echo "Lancer l'application en activant l'environnement virtuel :"
    echo "source venv/bin/activate"
    echo "uvicorn app.main:app --reload"
    echo 
    echo " - API:        http://localhost:8000/docs"
  fi
}

stop_services() {
  echo "🛑 Arrêt des services..."
  docker compose -f "$COMPOSE_FILE" down --volumes --remove-orphans
  echo "🧹 Nettoyage terminé"
}

# Main
check_docker
check_venv

case "$1" in
  --help)
    show_help
    ;;
  --stop)
    stop_services
    ;;
  *)
    start_services "$1" "$2"
    ;;
esac
