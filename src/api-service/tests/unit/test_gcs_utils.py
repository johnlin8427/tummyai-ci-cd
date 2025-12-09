"""
Unit tests for GCS utilities module
Tests the GCS bucket, blob, and CSV read/write functions
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from api.utils.utils import get_gcs_bucket, get_blob, read_csv_from_gcs, write_csv_to_gcs


class TestGetGcsBucket:
    """Tests for the get_gcs_bucket() function"""

    @patch("api.utils.utils.storage.Client")
    def test_get_gcs_bucket_success(self, mock_client_class):
        """Test get_gcs_bucket returns bucket correctly"""
        mock_client = mock_client_class.return_value
        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket

        with patch.dict("os.environ", {"GCS_BUCKET_NAME": "test-bucket"}):
            # Reset the cached bucket
            import api.utils.utils as utils_module
            utils_module._bucket = None

            bucket = get_gcs_bucket()
            assert bucket is mock_bucket

    @patch("api.utils.utils.storage.Client")
    def test_get_gcs_bucket_uses_env_var(self, mock_client_class):
        """Test get_gcs_bucket uses GCS_BUCKET_NAME environment variable"""
        mock_client = mock_client_class.return_value
        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket

        with patch.dict("os.environ", {"GCS_BUCKET_NAME": "my-custom-bucket"}):
            import api.utils.utils as utils_module
            utils_module._bucket = None

            get_gcs_bucket()
            mock_client.bucket.assert_called_with("my-custom-bucket")


class TestGetBlob:
    """Tests for the get_blob() function"""

    def test_get_blob_found(self):
        """Test get_blob returns blob when file exists"""
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "example.csv"
        mock_bucket.list_blobs.return_value = [mock_blob]

        with patch("api.utils.utils.get_gcs_bucket", return_value=mock_bucket):
            blob = get_blob("example.csv")
            assert blob.name == "example.csv"

    def test_get_blob_not_found(self):
        """Test get_blob raises HTTPException when file doesn't exist"""
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "other.csv"
        mock_bucket.list_blobs.return_value = [mock_blob]

        with patch("api.utils.utils.get_gcs_bucket", return_value=mock_bucket):
            with pytest.raises(HTTPException) as e:
                get_blob("nonexistent.csv")
            assert e.value.status_code == 404
            assert "File not found" in e.value.detail

    def test_get_blob_with_prefix(self):
        """Test get_blob with file path prefix"""
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "data/users/user123.csv"
        mock_bucket.list_blobs.return_value = [mock_blob]

        with patch("api.utils.utils.get_gcs_bucket", return_value=mock_bucket):
            blob = get_blob("data/users/user123.csv")
            assert blob.name == "data/users/user123.csv"


class TestReadCsvFromGcs:
    """Tests for the read_csv_from_gcs() function"""

    def test_read_csv_simple_float(self):
        """Test read_csv_from_gcs with normal float values"""
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "col1,col2\n1.0,2.0\n3.0,4.0"

        df = read_csv_from_gcs(mock_blob)

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["col1", "col2"]
        assert df.iloc[0]["col1"] == 1.0
        assert df.iloc[0]["col2"] == 2.0

    def test_read_csv_with_inf_float(self):
        """Test read_csv_from_gcs with inf and -inf values"""
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "col1,col2\n1.0,inf\n-inf,4.0"

        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == 1.0
        assert df.iloc[0]["col2"] is None
        assert df.iloc[1]["col1"] is None
        assert df.iloc[1]["col2"] == 4.0

    def test_read_csv_with_nan_float(self):
        """Test read_csv_from_gcs with missing float values"""
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "col1,col2\n1.0,\n,4.0"

        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == 1.0
        assert pd.isna(df.iloc[0]["col2"])
        assert pd.isna(df.iloc[1]["col1"])
        assert df.iloc[1]["col2"] == 4.0

    def test_read_csv_simple_str(self):
        """Test read_csv_from_gcs with normal string values"""
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "col1,col2\na,b\nc,d"

        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == "a"
        assert df.iloc[0]["col2"] == "b"
        assert df.iloc[1]["col1"] == "c"
        assert df.iloc[1]["col2"] == "d"

    def test_read_csv_with_nan_str(self):
        """Test read_csv_from_gcs with missing string values"""
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "col1,col2\na,\n,d"

        df = read_csv_from_gcs(mock_blob)

        assert df.iloc[0]["col1"] == "a"
        assert df.iloc[0]["col2"] is None
        assert df.iloc[1]["col1"] is None
        assert df.iloc[1]["col2"] == "d"


class TestWriteCsvToGcs:
    """Tests for the write_csv_to_gcs() function"""

    def test_write_csv_simple_float(self):
        """Test write_csv_to_gcs with simple float values"""
        mock_blob = MagicMock()
        df = pd.DataFrame({"col1": [1.0, 3.0], "col2": [2.0, 4.0]})

        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\n1.0,2.0\n3.0,4.0\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_with_inf_float(self):
        """Test write_csv_to_gcs with inf and -inf values"""
        mock_blob = MagicMock()
        df = pd.DataFrame({"col1": [1.0, float("-inf")], "col2": [float("inf"), 4.0]})

        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\n1.0,inf\n-inf,4.0\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_with_nan_float(self):
        """Test write_csv_to_gcs with missing float values"""
        mock_blob = MagicMock()
        df = pd.DataFrame({"col1": [1.0, None], "col2": [None, 4.0]})

        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\n1.0,\n,4.0\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_simple_str(self):
        """Test write_csv_to_gcs with simple string values"""
        mock_blob = MagicMock()
        df = pd.DataFrame({"col1": ["a", "c"], "col2": ["b", "d"]})

        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\na,b\nc,d\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")

    def test_write_csv_with_nan_str(self):
        """Test write_csv_to_gcs with missing string values"""
        mock_blob = MagicMock()
        df = pd.DataFrame({"col1": ["a", None], "col2": [None, "d"]})

        write_csv_to_gcs(mock_blob, df)

        expected_csv = "col1,col2\na,\n,d\n"
        mock_blob.upload_from_string.assert_called_once_with(expected_csv, content_type="text/csv")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
