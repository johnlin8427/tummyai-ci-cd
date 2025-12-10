"""
Food image analysis APIs
"""

import io
import os
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps
from fastapi import APIRouter

from api.utils.food_model_utils import (
    load_dish_to_ing_dict,
    load_ing_to_fodmap_dict,
    load_food_model,
    calculate_fodmap_level,
)

# Define router
router = APIRouter()

# Define variables
skip_download = os.getenv("SKIP_DOWNLOAD", "0")

# Load ingredients map and computer vision model once at startup
if skip_download == "1":
    dish_to_ing_dict = {}
    ing_to_fodmap_dict = {}
    classifier = None
else:
    dish_to_ing_dict = load_dish_to_ing_dict()
    ing_to_fodmap_dict = load_ing_to_fodmap_dict()
    classifier = load_food_model()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Check if model is loaded
        if classifier is None:
            return JSONResponse(content={"error": "Model not loaded (running in CI mode)"}, status_code=503)

        # Read uploaded image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Apply EXIF orientation correction (fixes phone image rotation)
        # exif_transpose returns None if image has no EXIF data, so use original image
        image = ImageOps.exif_transpose(image) or image

        # Convert to RGB after orientation correction
        image = image.convert("RGB")

        # Resize large images for consistent processing (max 1024x1024)
        # This helps with both memory usage and model consistency
        max_size = (1024, 1024)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Run model inference
        results = classifier(image)

        # Add FODMAP information based on prediction
        if results and len(results) > 0:
            predicted_food = results[0]["label"]
            confidence = results[0]["score"]

            # Get ingredients for predicted dish
            ingredients = dish_to_ing_dict.get(predicted_food.lower(), [])

            # Calculate FODMAP level based on actual ingredients
            fodmap_result = calculate_fodmap_level(ingredients, ing_to_fodmap_dict)

            return JSONResponse(
                content={
                    "dish": predicted_food,
                    "dish_confidence": confidence,
                    "dish_fodmap": fodmap_result["level"],  # "high", "moderate", "low", "unknown"
                    "ingredients": ", ".join(ingredients),
                    "ingredients_fodmap_high": ", ".join(fodmap_result["high_fodmap"]),
                    "ingredients_fodmap_low": ", ".join(fodmap_result["low_fodmap"]),
                    "ingredients_fodmap_none": ", ".join(fodmap_result["none_fodmap"]),
                }
            )
        else:
            return JSONResponse(content={"error": "No predictions available"}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
