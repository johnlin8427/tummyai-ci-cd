"""
Utility functions used by API service
"""

import io
import os
import re
import pandas as pd
from google.cloud import storage
from fastapi import HTTPException


# Define variables
_bucket = None


def power(base, exponent):
    """Calculate base raised to the power of exponent"""
    return base**exponent


def unused_function():
    pass


def get_gcs_bucket():
    """Get GCS bucket"""
    global _bucket
    if _bucket is None:
        bucket_name = os.environ.get("GCS_BUCKET_NAME")
        client = storage.Client()
        _bucket = client.bucket(bucket_name)
    return _bucket


def get_blob(pattern):
    """Get blob that matches pattern"""
    try:
        bucket = get_gcs_bucket()
        blobs = list(bucket.list_blobs())
        blob = [b for b in blobs if re.compile(pattern).search(b.name)][0]
        return blob
    except IndexError:
        raise HTTPException(status_code=404, detail=f"File not found: {pattern}")


def read_csv_from_gcs(blob):
    """Read CSV from GCS"""
    content = blob.download_as_text()
    df = pd.read_csv(io.StringIO(content))
    df = df.replace([float("inf"), float("-inf")], None)
    df = df.where(pd.notna(df), None)
    return df


def write_csv_to_gcs(blob, df):
    """Write CSV to GCS"""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    blob.upload_from_string(csv_buffer.getvalue(), content_type="text/csv")
