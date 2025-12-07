"""
Food image analysis APIs
"""

import io
import os
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
from fastapi import APIRouter

from api.utils.food_model_utils import load_ingredients_map, load_food_model

# Define router
router = APIRouter()

# Define variables
skip_download = os.getenv("SKIP_DOWNLOAD", "0")

# Load ingredients map and computer vision model once at startup
if skip_download == "1":
    ingredients_map = {}
    classifier = None
else:
    ingredients_map = load_ingredients_map()
    classifier = load_food_model()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict dish + ingredients from image"""
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
            ingredients = ingredients_map.get(predicted_food.lower(), [])

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
