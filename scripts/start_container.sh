#!/bin/bash
set -e

# pull the docker image from docker hub
docker pull SIVAGORAM/simple-python-flask-app:latest

# run the docker image as a container
docker run -d -p 5000:5000 SIVAGORAM/simple-python-flask-app:latest
