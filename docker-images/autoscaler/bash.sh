#!/bin/bash

# Remove the existing stack
sudo docker stack rm app_name

# Wait for the stack removal to complete
sleep 5

# Change directory to autoscaler

# Build the Docker image
sudo docker build -t auto:1 .

cd ../

# Deploy the stack
sudo docker stack deploy --compose-file docker-compose.yml app_name

# Wait for the stack to be deployed
sleep 5

# Show the logs
sudo docker service logs app_name_autoscaler

