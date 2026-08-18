#!/bin/bash
set -e

# Pull the Docker image from Docker Hub
echo "Pulling the latest Docker image..."
docker pull $DOCKER_REGISTRY_USERNAME/simple-python-flask-app:latest

# Run the Docker image as a container
echo "Running the Docker container..."
docker run -d -p 5000:5000 --name simple-python-flask-app $DOCKER_REGISTRY_USERNAME/simple-python-flask-app:latest
