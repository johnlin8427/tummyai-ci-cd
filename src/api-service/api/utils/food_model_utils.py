"""
Utility functions used by food image analysis APIs
"""

from pathlib import Path
from api.utils.utils import get_gcs_bucket, get_blob, read_csv_from_gcs


def load_ingredients_map() -> dict:
    """
    Download CSV file from GCS bucket that maps dish names to ingredient list.

    Returns:
        Dict mapping dish names to ingredient lists
    """
    try:
        # Read CSV from GCS
        print("⬇️ Downloading ingredients map from GCS...")
        pattern = "data/reference/dish_to_ingredients_cleaned.csv"
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


def download_model_from_gcs(bucket_name: str, model_version: str, local_dir: str) -> str:
    """
    Download model files from GCS bucket.

    Args:
        bucket_name: GCS bucket name
        model_version: Model version folder in GCS
        local_dir: Local directory to save model files

    Returns:
        Local path to the model
    """
    # Create local directory if it doesn't exist
    model_path = Path(local_dir)
    model_path.mkdir(parents=True, exist_ok=True)

    # List of model files to download
    model_files = ["config.json", "preprocessor_config.json", "model.safetensors"]

    print(f"⬇️  Downloading TummyAI model from GCS bucket: {bucket_name}/{model_version}")

    try:
        # Download each file
        bucket = get_gcs_bucket()
        for filename in model_files:
            gcs_path = f"{model_version}/{filename}"
            local_path = model_path / filename

            # Skip if file already exists
            if local_path.exists():
                print(f"   ✓ {filename} already exists locally")
                continue

            print(f"   ⬇️  Downloading {filename}...", end=" ")
            blob = bucket.blob(gcs_path)
            blob.download_to_filename(str(local_path))
            print("✓")

        print(f"✅ TummyAI model successfully downloaded to {local_dir}")
        return str(model_path)

    except Exception as e:
        print(f"❌ Error downloading model from GCS: {e}")
        raise


def verify_model_files(model_path: str) -> bool:
    """
    Verify that all required model files exist.

    Args:
        model_path: Path to model directory

    Returns:
        True if all files exist, False otherwise
    """
    required_files = ["config.json", "model.safetensors"]
    model_dir = Path(model_path)

    for filename in required_files:
        if not (model_dir / filename).exists():
            print(f"❌ Missing required file: {filename}")
            return False

    return True
