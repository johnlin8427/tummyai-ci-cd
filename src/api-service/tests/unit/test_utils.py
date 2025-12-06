"""
Unit tests for utils module
"""

import os
import pytest
import pandas as pd
import numpy as np
from fastapi import HTTPException
from unittest.mock import MagicMock, patch

from api.utils.utils import get_gcs_bucket, get_blob, read_csv_from_gcs, write_csv_to_gcs
from api.utils.health_report_utils import convert_onehot, run_fisher


@pytest.fixture
def mock_bucket():
    blob = MagicMock()
    blob.name = "example.csv"

    bucket = MagicMock()
    bucket.list_blobs.return_value = [blob]
    return bucket


@pytest.fixture
def mock_blob():
    blob = MagicMock()
    return blob


class TestGetBucket:
    """Tests for the get_gcs_bucket() function"""

    def test_get_gcs_bucket(self, mock_bucket):
        """Test get_gcs_bucket() with mock bucket"""
        with patch("api.utils.utils.storage.Client") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.bucket.return_value = mock_bucket

            os.environ["GCS_BUCKET_NAME"] = "test-bucket"

            # First call initializes _bucket
            bucket = get_gcs_bucket()
            assert bucket is mock_bucket


class TestGetBlob:
    """Tests for the get_blob() function"""

    def test_get_blob_found(self, mock_bucket):
        """Test get_blob() with existing blob"""
        with patch("api.utils.utils.get_gcs_bucket", return_value=mock_bucket):
            blob = get_blob("example.csv")
            assert blob.name == "example.csv"

    def test_get_blob_not_found(self, mock_bucket):
        """Test get_blob() with non-existing blob"""
        with patch("api.utils.utils.get_gcs_bucket", return_value=mock_bucket):
            with pytest.raises(HTTPException) as e:
                get_blob("nonexistent.csv")
                assert e.value.status_code == 404
        assert "File not found: nonexistent.csv" in e.value.detail


class TestReadCsv:
    """Tests for the read_csv_from_gcs() function"""

    def test_read_csv_simple_float(self, mock_blob):
        """Test read_csv_from_gcs() with normal float values"""
        mock_blob.download_as_text.return_value = "col1,col2\n1.0,2.0\n3.0,4.0"
        df = read_csv_from_gcs(mock_blob)

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["col1", "col2"]
        assert df.iloc[0]["col1"] == 1.0
        assert df.iloc[0]["col2"] == 2.0
        assert df.iloc[1]["col1"] == 3.0
        assert df.iloc[1]["col2"] == 4.0

    def test_read_csv_with_inf_float(self, mock_blob):
        """Test read_csv_from_gcs() with inf and -inf values"""
        mock_blob.download_as_text.return_value = "col1,col2\n1.0,inf\n-inf,4.0"
        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == 1.0
        assert df.iloc[0]["col2"] is None
        assert df.iloc[1]["col1"] is None
        assert df.iloc[1]["col2"] == 4.0

    def test_read_csv_with_nan_float(self, mock_blob):
        """Test read_csv_from_gcs() with missing float values"""
        mock_blob.download_as_text.return_value = "col1,col2\n1.0,\n,4.0"
        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == 1.0
        assert pd.isna(df.iloc[0]["col2"])
        assert pd.isna(df.iloc[1]["col1"])
        assert df.iloc[1]["col2"] == 4.0

    def test_read_csv_simple_str(self, mock_blob):
        """Test read_csv_from_gcs() with normal string values"""
        mock_blob.download_as_text.return_value = "col1,col2\na,b\nc,d"
        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == "a"
        assert df.iloc[0]["col2"] == "b"
        assert df.iloc[1]["col1"] == "c"
        assert df.iloc[1]["col2"] == "d"

    def test_read_csv_with_nan_str(self, mock_blob):
        """Test read_csv_from_gcs() with missing string values"""
        mock_blob.download_as_text.return_value = "col1,col2\na,\n,d"
        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == "a"
        assert df.iloc[0]["col2"] is None
        assert df.iloc[1]["col1"] is None
        assert df.iloc[1]["col2"] == "d"


class TestWriteCsv:
    """Tests for the write_csv_to_gcs() function"""

    def test_write_csv_simple_float(self, mock_blob):
        """Test write_csv_to_gcs() with simple float values"""
        df = pd.DataFrame({"col1": [1.0, 3.0], "col2": [2.0, 4.0]})
        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\n1.0,2.0\n3.0,4.0\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_with_inf_float(self, mock_blob):
        """Test write_csv_to_gcs() with inf and -inf values"""
        df = pd.DataFrame({"col1": [1.0, float("-inf")], "col2": [float("inf"), 4.0]})
        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\n1.0,inf\n-inf,4.0\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_with_nan_float(self, mock_blob):
        """Test write_csv_to_gcs() with missing float values"""
        df = pd.DataFrame({"col1": [1.0, None], "col2": [None, 4.0]})
        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\n1.0,\n,4.0\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_simple_str(self, mock_blob):
        """Test write_csv_to_gcs() with simple string values"""
        df = pd.DataFrame({"col1": ["a", "c"], "col2": ["b", "d"]})
        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\na,b\nc,d\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_with_nan_str(self, mock_blob):
        """Test write_csv_to_gcs() with missing string values"""
        df = pd.DataFrame({"col1": ["a", None], "col2": [None, "d"]})
        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\na,\n,d\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")


class TestConvertOnehot:
    """Tests for the convert_onehot() function"""

    def test_convert_onehot_simple(self):
        """Test convert_onehot() with simple input"""
        data = {
            "ingredients": ["milk, cheese", "cheese"],
            "symptoms": ["nausea", "headache, nausea"],
        }
        history = pd.DataFrame(data)
        onehot_df = convert_onehot(history)

        expected_columns = sorted(
            [
                "ingredient_cheese",
                "ingredient_milk",
                "symptom_headache",
                "symptom_nausea",
            ]
        )
        assert sorted(onehot_df.columns.tolist()) == expected_columns

        assert onehot_df.iloc[0]["ingredient_cheese"] == 1
        assert onehot_df.iloc[0]["ingredient_milk"] == 1
        assert onehot_df.iloc[0]["symptom_headache"] == 0
        assert onehot_df.iloc[0]["symptom_nausea"] == 1

        assert onehot_df.iloc[1]["ingredient_cheese"] == 1
        assert onehot_df.iloc[1]["ingredient_milk"] == 0
        assert onehot_df.iloc[1]["symptom_headache"] == 1
        assert onehot_df.iloc[1]["symptom_nausea"] == 1

    def test_convert_onehot_empty(self):
        """Test convert_onehot() with empty input"""
        history = pd.DataFrame({"ingredients": [], "symptoms": []})
        onehot_df = convert_onehot(history)
        assert onehot_df.empty


class TestRunFisher:
    """Tests for the run_fisher() function"""

    def test_run_fisher_simple(self):
        """Test run_fisher() with simple input"""
        data = {
            "ingredient_cheese": [1, 1, 0, 0],
            "ingredient_milk": [1, 0, 1, 0],
            "symptom_nausea": [1, 0, 1, 0],
        }
        history = pd.DataFrame(data)
        results_df = run_fisher(history)

        assert not results_df.empty
        expected_columns = {
            "symptom": str,
            "ingredient": str,
            "odds_ratio": float,
            "p_value": float,
            "p_value_adj": float,
            "significant": np.bool_,
        }
        for col, type in expected_columns.items():
            assert col in results_df.columns
            assert isinstance(results_df[col].iloc[0], type)

    def test_run_fisher_empty(self):
        """Test run_fisher() with empty input"""
        history = pd.DataFrame()
        results_df = run_fisher(history)
        assert results_df.empty
