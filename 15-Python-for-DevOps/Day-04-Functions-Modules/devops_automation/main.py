#!/usr/bin/env python3

# We are importing Modules from our custom 'deployment' Package
from deployment import aws
from deployment import docker

print("--- Starting Automation Pipeline ---")

# Calling Functions from the imported Modules
docker.build_image()
aws.deploy_to_aws()

print("--- Pipeline Completed Successfully ---")
