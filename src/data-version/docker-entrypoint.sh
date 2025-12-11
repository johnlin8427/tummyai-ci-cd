#!/bin/bash

set -e

echo "Container is running!!!"

# Mount GCS bucket
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
mkdir -p /mnt/gcs_bucket
gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS $GCS_BUCKET_NAME /mnt/gcs_bucket
echo 'GCS bucket mounted at /mnt/gcs_bucket'
mkdir -p /app/gcs_data
mount --bind /mnt/gcs_bucket/data_version /app/gcs_data

# Activate virtual environment
echo "Activating virtual environment..."
source /.venv/bin/activate

# Mark /app as a safe Git directory
git config --global --add safe.directory /app

# If arguments are passed, execute them instead of starting the server
if [ $# -gt 0 ]; then
  echo "Executing command: $@"
  exec "$@"
fi

# Otherwise, start an interactive bash shell
echo "Starting interactive /bin/bash shell"
exec /bin/bash
