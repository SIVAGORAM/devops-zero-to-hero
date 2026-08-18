#!/bin/bash
set -e

# Stop the running container (if any)
echo "Stopping any existing containers..."
container_id=$(docker ps -q --filter "name=simple-python-flask-app")

if [ -n "$container_id" ]; then
    echo "Stopping container $container_id"
    docker stop $container_id
    docker rm $container_id
else
    echo "No existing container found."
fi
