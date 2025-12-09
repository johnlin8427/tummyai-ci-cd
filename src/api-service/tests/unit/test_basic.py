"""
Unit tests for basic functionality and imports
"""
import sys
import pytest


def test_python_version():
    """Test that Python version is 3.10 or higher"""
    assert sys.version_info >= (3, 10), f"Python version must be >= 3.10, got {sys.version_info}"


def test_fastapi_import():
    """Test that FastAPI can be imported"""
    try:
        import fastapi

        assert fastapi is not None
        assert hasattr(fastapi, "FastAPI")
    except ImportError as e:
        pytest.fail(f"Failed to import FastAPI: {e}")


def test_transformers_import():
    """Test that transformers library can be imported"""
    try:
        import transformers

        assert transformers is not None
        assert hasattr(transformers, "pipeline")
    except ImportError as e:
        pytest.fail(f"Failed to import transformers: {e}")


def test_torch_import():
    """Test that PyTorch can be imported"""
    try:
        import torch

        assert torch is not None
        assert hasattr(torch, "tensor")
    except ImportError as e:
        pytest.fail(f"Failed to import torch: {e}")


def test_pil_import():
    """Test that PIL (Pillow) can be imported"""
    try:
        from PIL import Image

        assert Image is not None
    except ImportError as e:
        pytest.fail(f"Failed to import PIL: {e}")


def test_pandas_import():
    """Test that pandas can be imported"""
    try:
        import pandas

        assert pandas is not None
        assert hasattr(pandas, "DataFrame")
    except ImportError as e:
        pytest.fail(f"Failed to import pandas: {e}")


def test_google_cloud_storage_import():
    """Test that google-cloud-storage can be imported"""
    try:
        from google.cloud import storage

        assert storage is not None
        assert hasattr(storage, "Client")
    except ImportError as e:
        pytest.fail(f"Failed to import google.cloud.storage: {e}")


def test_utils_module_import():
    """Test that utils module can be imported"""
    try:
        from api.utils.utils import get_gcs_bucket, get_blob, read_csv_from_gcs, write_csv_to_gcs

        assert get_gcs_bucket is not None
        assert get_blob is not None
        assert read_csv_from_gcs is not None
        assert write_csv_to_gcs is not None
    except ImportError as e:
        pytest.fail(f"Failed to import utils module: {e}")


def test_health_report_utils_import():
    """Test that health_report_utils module can be imported"""
    try:
        from api.utils.health_report_utils import convert_onehot, run_fisher

        assert convert_onehot is not None
        assert run_fisher is not None
    except ImportError as e:
        pytest.fail(f"Failed to import health_report_utils: {e}")


def test_food_model_utils_import():
    """Test that food_model_utils module can be imported"""
    try:
        from api.utils.food_model_utils import load_dish_to_ing_dict, load_ing_to_fodmap_dict

        assert load_dish_to_ing_dict is not None
        assert load_ing_to_fodmap_dict is not None
    except ImportError as e:
        pytest.fail(f"Failed to import food_model_utils: {e}")


def test_service_app_import():
    """Test that the main service app can be imported"""
    try:
        from api.service import app

        assert app is not None
    except ImportError as e:
        pytest.fail(f"Failed to import service app: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
