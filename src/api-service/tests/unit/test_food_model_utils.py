"""
Unit tests for food model utility functions
"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from api.utils.food_model_utils import (
    normalize_ingredient_list,
    calculate_fodmap_level,
    verify_model_files,
    download_model_from_gcs,
    load_dish_to_ing_dict,
    load_ing_to_fodmap_dict,
)


class TestNormalizeIngredientList:
    """Test ingredient string parsing function"""

    def test_python_list_format(self):
        """Test parsing Python list format strings"""
        # Standard Python list
        result = normalize_ingredient_list("['apples', 'sugar', 'flour']")
        assert result == ["apples", "sugar", "flour"]

        # List with extra spaces
        result = normalize_ingredient_list("['  apples  ', '  sugar  ']")
        assert result == ["apples", "sugar"]

        # List with mixed quotes
        result = normalize_ingredient_list('["apples", "sugar"]')
        assert result == ["apples", "sugar"]

    def test_comma_separated_format(self):
        """Test parsing comma-separated strings"""
        result = normalize_ingredient_list("apples, sugar, flour")
        assert result == ["apples", "sugar", "flour"]

        # With extra spaces
        result = normalize_ingredient_list("  apples  ,  sugar  ,  flour  ")
        assert result == ["apples", "sugar", "flour"]

    def test_semicolon_separated(self):
        """Test parsing semicolon-separated strings"""
        result = normalize_ingredient_list("apples; sugar; flour")
        assert result == ["apples", "sugar", "flour"]

    def test_pipe_separated(self):
        """Test parsing pipe-separated strings"""
        result = normalize_ingredient_list("apples | sugar | flour")
        assert result == ["apples", "sugar", "flour"]

    def test_mixed_case_normalization(self):
        """Test that all ingredients are lowercased"""
        result = normalize_ingredient_list("APPLES, Sugar, FLoUr")
        assert result == ["apples", "sugar", "flour"]

    def test_empty_string(self):
        """Test handling of empty strings"""
        result = normalize_ingredient_list("")
        assert result == []

    def test_malformed_list(self):
        """Test handling of malformed list syntax"""
        # Unclosed bracket - should fall back to generic parser
        result = normalize_ingredient_list("['apples', 'sugar'")
        assert len(result) > 0  # Should still parse something

    def test_single_ingredient(self):
        """Test single ingredient parsing"""
        result = normalize_ingredient_list("apple")
        assert result == ["apple"]

        result = normalize_ingredient_list("['apple']")
        assert result == ["apple"]


class TestCalculateFodmapLevel:
    """Test FODMAP level calculation function"""

    def test_high_fodmap_classification(self):
        """Test dishes with high FODMAP ingredients are classified as high"""
        ingredients = ["rice", "garlic", "onion", "beef"]
        fodmap_lookup = {
            "rice": "low",
            "garlic": "high",
            "onion": "high",
            "beef": "none"
        }

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        assert result["level"] == "high"
        assert "garlic" in result["high_fodmap"]
        assert "onion" in result["high_fodmap"]
        assert "rice" in result["low_fodmap"]
        assert len(result["details"]["high"]) == 2

    def test_moderate_fodmap_classification(self):
        """Test dishes with multiple low FODMAP ingredients (no high) are moderate"""
        ingredients = ["rice", "spinach", "carrot", "lettuce"]
        fodmap_lookup = {
            "rice": "low",
            "spinach": "low",
            "carrot": "low",
            "lettuce": "low"
        }

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        assert result["level"] == "moderate"
        assert len(result["details"]["low"]) == 4

    def test_low_fodmap_classification(self):
        """Test dishes with 1-2 low FODMAP ingredients are low"""
        ingredients = ["rice", "beef"]
        fodmap_lookup = {
            "rice": "low",
            "beef": "none"
        }

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        assert result["level"] == "low"
        assert len(result["details"]["low"]) == 1

    def test_only_none_ingredients(self):
        """Test dishes with only 'none' FODMAP ingredients"""
        ingredients = ["beef", "chicken", "oil"]
        fodmap_lookup = {
            "beef": "none",
            "chicken": "none",
            "oil": "none"
        }

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        assert result["level"] == "none"
        assert len(result["details"]["none"]) == 3

    def test_unknown_ingredients(self):
        """Test handling of unknown ingredients"""
        ingredients = ["mystery_food", "alien_ingredient"]
        fodmap_lookup = {}

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        assert result["level"] == "unknown"
        assert len(result["details"]["unknown"]) == 2

    def test_mixed_known_unknown(self):
        """Test mixture of known and unknown ingredients"""
        ingredients = ["rice", "mystery_food", "garlic"]
        fodmap_lookup = {
            "rice": "low",
            "garlic": "high"
        }

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        # Should be high because of garlic
        assert result["level"] == "high"
        assert "mystery_food" in result["details"]["unknown"]

    def test_empty_ingredients_list(self):
        """Test handling of empty ingredients list"""
        result = calculate_fodmap_level([], {})

        assert result["level"] == "unknown"
        assert result["details"]["high"] == []
        assert result["details"]["low"] == []

    def test_case_insensitive_lookup(self):
        """Test that ingredient lookup is case-insensitive"""
        ingredients = ["GARLIC", "Rice", "oNiOn"]
        fodmap_lookup = {
            "garlic": "high",
            "rice": "low",
            "onion": "high"
        }

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        assert result["level"] == "high"
        assert len(result["details"]["high"]) == 2
        assert len(result["details"]["low"]) == 1

    def test_return_structure(self):
        """Test the return dictionary has correct structure"""
        ingredients = ["rice", "garlic"]
        fodmap_lookup = {"rice": "low", "garlic": "high"}

        result = calculate_fodmap_level(ingredients, fodmap_lookup)

        # Check all required keys exist
        assert "level" in result
        assert "details" in result
        assert "high_fodmap" in result
        assert "low_fodmap" in result

        # Check details structure
        assert "high" in result["details"]
        assert "low" in result["details"]
        assert "none" in result["details"]
        assert "unknown" in result["details"]


class TestVerifyModelFiles:
    """Test model file verification function"""

    def test_verify_model_files_success(self):
        """Test that verify_model_files returns True when all files exist"""
        with patch("api.utils.food_model_utils.Path") as mock_path:
            mock_model_dir = MagicMock()
            mock_path.return_value = mock_model_dir

            # Mock that both required files exist
            mock_file = MagicMock()
            mock_file.exists.return_value = True
            mock_model_dir.__truediv__.return_value = mock_file

            result = verify_model_files("/fake/model/path")

            assert result is True

    def test_verify_model_files_missing_config(self):
        """Test that verify_model_files returns False when config.json is missing"""
        with patch("api.utils.food_model_utils.Path") as mock_path:
            mock_model_dir = MagicMock()
            mock_path.return_value = mock_model_dir

            mock_file = MagicMock()
            mock_file.exists.side_effect = [False, True]
            mock_model_dir.__truediv__.return_value = mock_file

            result = verify_model_files("/fake/model/path")

            assert result is False

    def test_verify_model_files_missing_safetensors(self):
        """Test that verify_model_files returns False when model.safetensors is missing"""
        with patch("api.utils.food_model_utils.Path") as mock_path:
            mock_model_dir = MagicMock()
            mock_path.return_value = mock_model_dir

            mock_file = MagicMock()
            mock_file.exists.side_effect = [True, False]
            mock_model_dir.__truediv__.return_value = mock_file

            result = verify_model_files("/fake/model/path")

            assert result is False


class TestLoadDishToIngDict:
    """Test dish-to-ingredient dictionary loading from GCS"""

    @patch("api.utils.food_model_utils.storage.Client")
    def test_successful_load(self, mock_storage_client):
        """Test successful loading of dish-to-ingredient mappings from GCS"""
        csv_content = """bibimbap,"['rice', 'beef', 'spinach']"
waffles,wheat flour, milk, eggs
"""
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = csv_content

        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value = mock_client

        result = load_dish_to_ing_dict()

        assert "bibimbap" in result
        assert "waffles" in result

    @patch("api.utils.food_model_utils.storage.Client")
    def test_load_failure_returns_empty_dict(self, mock_storage_client):
        """Test that load failures return empty dict"""
        mock_storage_client.side_effect = Exception("GCS error")

        result = load_dish_to_ing_dict()

        assert result == {}


class TestLoadIngToFodmapDict:
    """Test ingredient-to-FODMAP dictionary loading from GCS"""

    @patch("api.utils.food_model_utils.storage.Client")
    def test_successful_load(self, mock_storage_client):
        """Test successful loading of FODMAP lookup from GCS"""
        csv_content = """ingredient,fodmap
garlic,high
onion,high
rice,low
beef,none
"""
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = csv_content

        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value = mock_client

        result = load_ing_to_fodmap_dict()

        assert result["garlic"] == "high"
        assert result["onion"] == "high"
        assert result["rice"] == "low"
        assert result["beef"] == "none"

    @patch("api.utils.food_model_utils.storage.Client")
    def test_load_failure_returns_empty_dict(self, mock_storage_client):
        """Test that load failures return empty dict"""
        mock_storage_client.side_effect = Exception("GCS error")

        result = load_ing_to_fodmap_dict()

        assert result == {}

    @patch("api.utils.food_model_utils.storage.Client")
    def test_lowercase_normalization(self, mock_storage_client):
        """Test that ingredients and FODMAP levels are lowercased"""
        csv_content = """ingredient,fodmap
GARLIC,HIGH
Rice,Low
"""
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = csv_content

        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value = mock_client

        result = load_ing_to_fodmap_dict()

        assert result["garlic"] == "high"
        assert result["rice"] == "low"


class TestDownloadModelFromGcs:
    """Test model download from GCS"""

    @patch("api.utils.food_model_utils.get_gcs_bucket")
    @patch("api.utils.food_model_utils.Path")
    def test_download_creates_directory(self, mock_path, mock_get_bucket):
        """Test that download creates the model directory"""
        mock_model_dir = MagicMock()
        mock_path.return_value = mock_model_dir

        mock_file_path = MagicMock()
        mock_file_path.exists.return_value = True  # Skip downloads
        mock_model_dir.__truediv__.return_value = mock_file_path

        mock_bucket = MagicMock()
        mock_get_bucket.return_value = mock_bucket

        download_model_from_gcs("test-bucket", "models/v1", "/fake/path")

        mock_model_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch("api.utils.food_model_utils.get_gcs_bucket")
    @patch("api.utils.food_model_utils.Path")
    def test_skip_existing_files(self, mock_path, mock_get_bucket):
        """Test that existing files are skipped during download"""
        mock_model_dir = MagicMock()
        mock_path.return_value = mock_model_dir

        mock_file_path = MagicMock()
        mock_file_path.exists.return_value = True
        mock_model_dir.__truediv__.return_value = mock_file_path

        mock_bucket = MagicMock()
        mock_get_bucket.return_value = mock_bucket

        result = download_model_from_gcs("test-bucket", "models/v1", "/fake/path")

        # No downloads should occur since files exist
        mock_bucket.blob.assert_not_called()
        assert result == str(mock_model_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
