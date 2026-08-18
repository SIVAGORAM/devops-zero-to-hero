#!/bin/bash
set -e

# stop the running container (if any)
echo "Hi"

# Get the running container ID and remove it
containerid=$(docker ps -q)

if [ -n "$containerid" ]; then
    echo "Removing container $containerid"
    docker rm -f $containerid
else
    echo "No running containers found."
fi
