"""
Utility functions used by food image analysis APIs
"""

import os
from pathlib import Path
from transformers import pipeline
from api.utils.utils import get_gcs_bucket, get_blob, read_csv_from_gcs


# Define variables
gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
map_gcs_path = "data/reference/dish_to_ingredients_cleaned.csv"
model_gcs_path = "models/v1"
model_local_path = "models"


def load_ingredients_map() -> dict:
    """
    Download CSV file from GCS bucket that maps dish names to ingredient list.

    Returns:
        Dict mapping dish names to ingredient lists
    """
    try:
        # Read CSV from GCS
        print("⬇️ Downloading ingredients map from GCS...")
        pattern = map_gcs_path
        blob = get_blob(pattern)
        df = read_csv_from_gcs(blob)

        # Parse CSV
        print("🛠️ Parsing ingredients map..")
        ingredients_map = {row["dish"].lower(): eval(row["ingredients"]) for _, row in df.iterrows()}

        print(f"✅ Loaded {len(ingredients_map)} ingredients map")
        return ingredients_map

    except Exception as e:
        print(f"⚠️ Failed to load ingredients map: {e}")
        print("Continuing with empty ingredients map...")
        return {}


def load_food_model():
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
