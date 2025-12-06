"""
Food image analysis APIs
"""

import io
import os
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from transformers import pipeline
from PIL import Image
from fastapi import APIRouter

from api.utils.food_model_utils import download_model_from_gcs, verify_model_files, load_ingredients_map

# Define router
router = APIRouter()

# Load our fine-tuned model once at startup
model_path = os.getenv("MODEL_PATH", "models/food_model_finetuned")
gcs_bucket = os.getenv("GCS_BUCKET_NAME", "tummyai-data-versioning")
model_version = os.getenv("MODEL_VERSION", "model/v1")
skip_model_download = os.getenv("SKIP_MODEL_DOWNLOAD", "0") == "1"

# Load ingredients map once at startup
INGREDIENTS_MAP = {} if skip_model_download else load_ingredients_map()

# Initialize classifier as None for conditional loading
classifier = None

# Only download and load model if not in CI mode
if not skip_model_download:
    # Download model from GCS if not already present
    if not verify_model_files(model_path):
        print("⬇️  Model not found locally, downloading from GCS...")
        download_model_from_gcs(bucket_name=gcs_bucket, model_version=model_version, local_dir=model_path)

    # Verify model files exist
    if not verify_model_files(model_path):
        raise FileNotFoundError(f"TummyAI fine-tuned model not found at {model_path}. Model download may have failed.")

    print(f"✅ Loading TummyAI fine-tuned model from {model_path}")
    classifier = pipeline("image-classification", model=model_path)
else:
    print("⚠️  Skipping model download and loading (CI mode)")
    classifier = None


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict food item from uploaded image"""
    try:
        # Check if model is loaded
        if classifier is None:
            return JSONResponse(content={"error": "Model not loaded (running in CI mode)"}, status_code=503)

        # Read uploaded image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Run model inference
        results = classifier(image)

        # Add FODMAP information based on prediction
        if results and len(results) > 0:
            predicted_food = results[0]["label"]
            confidence = results[0]["score"]

            # Simple FODMAP mapping (expand this based on your needs)
            fodmap_mapping = {
                "waffles": "moderate",
                "bibimbap": "low",
                "chicken wings": "low",
                # Add more mappings as needed
            }

            fodmap_level = fodmap_mapping.get(predicted_food.lower(), "unknown")

            # Get ingredients for predicted dish
            ingredients = INGREDIENTS_MAP.get(predicted_food.lower(), [])

            return JSONResponse(
                content={
                    "predicted_class": predicted_food,
                    "confidence": confidence,
                    "ingredients": ingredients,
                    "fodmap_level": fodmap_level,
                    "all_predictions": results[:5],  # Top 5 predictions
                }
            )
        else:
            return JSONResponse(content={"error": "No predictions available"}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
