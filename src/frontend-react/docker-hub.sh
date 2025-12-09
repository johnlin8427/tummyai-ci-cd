#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="tummyai-app-frontend-react"
export BASE_DIR=$(pwd)

# Default values
DOCKER_USERNAME="johnlin8427"


echo "Docker Username: $DOCKER_USERNAME"


echo "Building production image..."

# Check if multi-arch builder exists and remove it if it does
if docker buildx inspect multi-arch >/dev/null 2>&1; then
    echo "Removing existing multi-arch builder..."
    docker buildx rm multi-arch
fi

# Setup multi architecture build
echo "Creating new multi-arch builder..."
docker buildx create --driver-opt network=host --use --name multi-arch

# Build and push multi-arch image
echo "Building and pushing multi-arch image..."
docker buildx build --platform linux/amd64 --push -t $DOCKER_USERNAME/$IMAGE_NAME -f Dockerfile .

echo "Production build complete and pushed to registry"
