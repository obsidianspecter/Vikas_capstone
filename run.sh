#!/bin/bash

# Stop any running containers
docker-compose down

# Remove any existing containers and volumes
docker-compose rm -f
docker volume prune -f

# Build and start the containers
docker-compose up --build

# To run the application directly (uncomment the line below)
# python3 app.py 