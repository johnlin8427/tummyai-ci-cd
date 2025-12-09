"""
Pytest configuration file
Sets up environment variables and fixtures for all tests
"""
import os

# Set environment variables BEFORE any imports
# This prevents model downloads during testing
os.environ["SKIP_DOWNLOAD"] = "1"
os.environ["GCS_BUCKET_NAME"] = "test-bucket"


def pytest_configure(config):
    """Called after command line options have been parsed and all plugins have been loaded."""
    # Ensure environment variables are set
    os.environ.setdefault("SKIP_DOWNLOAD", "1")
    os.environ.setdefault("GCS_BUCKET_NAME", "test-bucket")
