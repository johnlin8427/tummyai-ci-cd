"""
Utility functions used by food image analysis APIs
"""

import os
import re
import ast
import csv
from io import StringIO
from pathlib import Path
from google.cloud import storage
from transformers import pipeline

from api.utils.utils import get_gcs_bucket


# Define variables
gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
dish_to_ing_gcs_path = "data/reference/dish_to_ingredients.csv"
ing_to_fodmap_gcs_path = "data/reference/ingredient_to_fodmap.csv"
model_gcs_path = "models/v2"
model_local_path = "/tmp/models"


def load_dish_to_ing_dict() -> dict:
    """
    Download CSV file from GCS bucket that maps dish name to ingredients list.

    Returns:
        Dict mapping dish name to ingredients list
    """
    try:
        print("⬇️  Downloading dish-to-ingredient mappings from GCS...")

        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(gcs_bucket_name)
        blob = bucket.blob(dish_to_ing_gcs_path)

        # Download CSV as text
        csv_content = blob.download_as_text()

        # Parse CSV
        dish_to_ing_dict = {}
        lines = csv_content.strip().split("\n")

        for line in lines:
            # Split on first comma only (dish,ingredients)
            parts = line.split(",", 1)
            if len(parts) == 2:
                dish = parts[0].strip().lower()
                ingredients_str = parts[1].strip()

                # Parse ingredients using robust parser
                ingredients = normalize_ingredient_list(ingredients_str)
                dish_to_ing_dict[dish] = ingredients

        print(f"✅ Loaded {len(dish_to_ing_dict)} dish-to-ingredient mappings")
        return dish_to_ing_dict

    except Exception as e:
        print(f"⚠️ Failed to load dish-to-ingredient mappings: {e}")
        print("Continuing with empty dish-to-ingredient mappings...")
        return {}


def load_ing_to_fodmap_dict() -> dict:
    """
    Download CSV file from GCS bucket that maps ingredient to FODMAP level.

    Returns:
        Dict mapping ingredient to FODMAP level ("high", "low", "none", or None)
    """
    try:
        print("⬇️  Downloading ingredient-to-FODMAP mappings from GCS...")

        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(gcs_bucket_name)
        blob = bucket.blob(ing_to_fodmap_gcs_path)

        # Download CSV as text
        csv_content = blob.download_as_text()

        # Parse CSV with header: ingredient,fodmap
        fodmap_dict = {}
        reader = csv.DictReader(StringIO(csv_content))

        for row in reader:
            ingredient = row["ingredient"].strip().lower()
            fodmap_level = row["fodmap"].strip().lower()
            fodmap_dict[ingredient] = fodmap_level

        print(f"✅ Loaded {len(fodmap_dict)} ingredient-to-FODMAP mappings")
        return fodmap_dict

    except Exception as e:
        print(f"⚠️  Failed to load ingredient-to-FODMAP mappings: {e}")
        print("   Continuing with empty ingredient-to-FODMAP mappings...")
        return {}


def load_food_model():
    """
    Load model that maps food image to dish name.

    Returns:
        Model
    """
    # Download model from GCS if not already present
    if not verify_model_files(model_local_path):
        print("⬇️ Model not found locally, downloading from GCS...")
        download_model_from_gcs(gcs_bucket_name, model_gcs_path, model_local_path)

    # Verify model files exist
    if not verify_model_files(model_local_path):
        raise FileNotFoundError(
            f"TummyAI fine-tuned model not found at {model_local_path}. Model download may have failed."
        )

    print(f"✅ Loading TummyAI fine-tuned model from {model_local_path}")
    classifier = pipeline("image-classification", model=model_local_path)
    return classifier


def normalize_ingredient_list(ingredient_str: str) -> list:
    """
    Parse ingredient string into clean list of ingredients.
    Handles both Python list format and comma-separated format.

    Args:
        ingredient_str: Raw ingredient string from CSV

    Returns:
        List of normalized ingredient names (lowercase, trimmed)
    """
    s = str(ingredient_str).strip()
    clean_items = []

    # Case 1: Python list format "['apples', 'sugar']"
    if s.startswith("[") and s.endswith("]"):
        try:
            parsed = ast.literal_eval(s)
            for item in parsed:
                item = str(item).strip().lower()
                item = re.sub(r"^[\[\]'\" ]+|[\[\]'\" ]+$", "", item)
                if item:
                    clean_items.append(item)
            return clean_items
        except Exception:
            pass  # Fall through to generic parser

    # Case 2: Comma-separated format "apples, sugar, flour"
    parts = re.split(r",|;|\|", s)
    for p in parts:
        p = p.strip().lower()
        p = re.sub(r"^[\[\]'\" ]+|[\[\]'\" ]+$", "", p)
        if p:
            clean_items.append(p)

    return clean_items


def download_model_from_gcs(gcs_bucket_name: str, model_gcs_path: str, model_local_path: str) -> str:
    """
    Download model files from GCS bucket.

    Args:
        gcs_bucket_name: GCS bucket name
        model_gcs_path: Model version folder in GCS
        model_local_path: Local directory to save model files

    Returns:
        Local path to the model
    """
    # Create local directory if it doesn't exist
    model_local_path = Path(model_local_path)
    model_local_path.mkdir(parents=True, exist_ok=True)

    # List of model files to download
    model_files = ["config.json", "preprocessor_config.json", "model.safetensors"]

    print(f"⬇️ Downloading TummyAI model from GCS bucket: {gcs_bucket_name}/{model_gcs_path}")

    try:
        # Download each file
        bucket = get_gcs_bucket()
        for filename in model_files:
            gcs_path = f"{model_gcs_path}/{filename}"
            local_path = model_local_path / filename

            # Skip if file already exists
            if local_path.exists():
                print(f"   ✓ {filename} already exists locally")
                continue

            print(f"   ⬇️ Downloading {filename}...", end=" ")
            blob = bucket.blob(gcs_path)
            blob.download_to_filename(str(local_path))
            print("✓")

        print(f"✅ TummyAI model successfully downloaded to {model_local_path}")
        return str(model_local_path)

    except Exception as e:
        print(f"❌ Error downloading model from GCS: {e}")
        raise


def verify_model_files(model_local_path: str) -> bool:
    """
    Verify that all required model files exist.

    Args:
        model_local_path: Path to model directory

    Returns:
        True if all files exist, False otherwise
    """
    required_files = ["config.json", "model.safetensors"]
    model_dir = Path(model_local_path)

    for filename in required_files:
        if not (model_dir / filename).exists():
            print(f"❌ Missing required file: {filename}")
            return False

    return True


def calculate_fodmap_level(ingredients: list, fodmap_lookup: dict) -> dict:
    """
    Calculate overall FODMAP level for a dish based on its ingredients.

    Args:
        ingredients: List of ingredient names
        fodmap_lookup: Dict mapping ingredients to FODMAP levels

    Returns:
        Dict with:
        - "level": Overall FODMAP level ("high", "moderate", "low", "unknown")
        - "details": Breakdown by FODMAP level
        - "high_fodmap": List of high FODMAP ingredients
        - "low_fodmap": List of low FODMAP ingredients
    """
    breakdown = {"high": [], "low": [], "none": [], "unknown": []}

    for ing in ingredients:
        ing_lower = ing.lower().strip()
        level = fodmap_lookup.get(ing_lower, None)

        if level == "high":
            breakdown["high"].append(ing)
        elif level == "low":
            breakdown["low"].append(ing)
        elif level == "none":
            breakdown["none"].append(ing)
        else:
            breakdown["unknown"].append(ing)

    # Determine overall FODMAP level
    high_count = len(breakdown["high"])
    low_count = len(breakdown["low"])
    none_count = len(breakdown["none"])
    total_known = high_count + low_count + none_count

    if total_known == 0:
        overall_level = "unknown"
    elif high_count > 0:
        # If any high FODMAP ingredients, dish is high
        overall_level = "high"
    elif low_count > 2:
        # If multiple low FODMAP ingredients, dish is moderate
        overall_level = "moderate"
    elif low_count > 0:
        # Some low FODMAP ingredients
        overall_level = "low"
    else:
        # Only "none" ingredients
        overall_level = "none"

    return {
        "level": overall_level,
        "details": breakdown,
        "high_fodmap": breakdown["high"],
        "low_fodmap": breakdown["low"],
        "none_fodmap": breakdown["none"],
    }
