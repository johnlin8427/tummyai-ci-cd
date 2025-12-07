#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="tummyai-app-api-service"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export PERSISTENT_DIR=$(pwd)/../../../persistent-folder/
export GCP_PROJECT="tummyai-ci-cd"
export GCS_BUCKET_NAME="tummyai-app-models"

# Create the network if we don't have it yet
docker network inspect tummyai-app-network >/dev/null 2>&1 || docker network create tummyai-app-network

# Build the image based on the Dockerfile
# docker build -t $IMAGE_NAME -f Dockerfile .

# # Run the container
# docker run -d --name api-server -p 9000:9000 \
# -e DEV=1 \
# -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-service.json \
# -e GCP_PROJECT=$GCP_PROJECT \
# -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
# -v "$SECRETS_DIR":/secrets \
# $IMAGE_NAME

# Run the container
docker run --rm \
--network host \
$IMAGE_NAME pytest tests/system/ -v --tb=short

# # Run the container
# docker run --rm --name $IMAGE_NAME -ti \
# -v "$BASE_DIR":/app \
# -v "$SECRETS_DIR":/secrets \
# -v "$PERSISTENT_DIR":/persistent \
# -p 9000:9000 \
# -e DEV=1 \
# -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-service.json \
# -e GCP_PROJECT=$GCP_PROJECT \
# -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
# --network tummyai-app-network \
# $IMAGE_NAME
