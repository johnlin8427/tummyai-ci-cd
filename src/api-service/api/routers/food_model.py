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
        
        # Log file info for debugging
        file_size_kb = len(image_bytes) / 1024
        print(f"📸 Received image: {file.filename}, size: {file_size_kb:.1f}KB, content_type: {file.content_type}")
        
        # Check file size (limit to 10MB)
        if len(image_bytes) > 10 * 1024 * 1024:
            return JSONResponse(content={"error": "Image too large. Maximum size is 10MB."}, status_code=400)
        
        # Check if file is empty
        if len(image_bytes) == 0:
            return JSONResponse(content={"error": "Empty file received"}, status_code=400)

        try:
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as img_err:
            print(f"❌ Failed to open image: {img_err}")
            return JSONResponse(content={"error": f"Invalid image format: {str(img_err)}"}, status_code=400)

        # Log original image info
        print(f"📐 Original image size: {image.size}, mode: {image.mode}, format: {image.format}")

        # Apply EXIF orientation correction (fixes phone image rotation)
        # exif_transpose returns None if image has no EXIF data, so use original image
        try:
            transposed = ImageOps.exif_transpose(image)
            if transposed is not None:
                image = transposed
                print("🔄 Applied EXIF orientation correction")
        except Exception as exif_err:
            print(f"⚠️ EXIF transpose failed (continuing with original): {exif_err}")

        # Convert to RGB after orientation correction (handles RGBA, P, L modes)
        if image.mode != "RGB":
            print(f"🎨 Converting from {image.mode} to RGB")
            image = image.convert("RGB")

        # Resize large images for consistent processing (max 1024x1024)
        # This helps with both memory usage and model consistency
        max_size = (1024, 1024)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            original_size = image.size
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            print(f"📏 Resized from {original_size} to {image.size}")

        # Run model inference
        print("🤖 Running model inference...")
        results = classifier(image)

        # Add FODMAP information based on prediction
        if results and len(results) > 0:
            predicted_food = results[0]["label"]
            confidence = results[0]["score"]
            print(f"✅ Prediction: {predicted_food} (confidence: {confidence:.2%})")

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
            print("⚠️ No predictions returned from model")
            return JSONResponse(content={"error": "No predictions available"}, status_code=500)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Error in predict endpoint: {e}\n{error_details}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
