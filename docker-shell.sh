#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define environment variables
export IMAGE_NAME="tummy-app-api-service"

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME -f Dockerfile .

# Start an interactive bash shell in the container
echo "Starting interactive container shell: $IMAGE_NAME"
docker run --rm -ti \
  --name $IMAGE_NAME \
  -p 9000:9000 \
  $IMAGE_NAME /bin/bash
