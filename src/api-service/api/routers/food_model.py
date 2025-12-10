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

# Try to import HEIC support for iPhone images
try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
    HEIC_SUPPORTED = True
    print("✅ HEIC support enabled for iPhone images")
except ImportError:
    HEIC_SUPPORTED = False
    print("⚠️ HEIC support not available (pillow-heif not installed)")

# Define router
router = APIRouter()

# Define variables
skip_download = os.getenv("SKIP_DOWNLOAD", "0")

# Max image size for processing (pixels) - smaller = faster inference
MAX_IMAGE_SIZE = 512


def safe_load_image(image_bytes: bytes, filename: str = "") -> Image.Image:
    """
    Safely load and preprocess an image from bytes.
    Handles EXIF orientation, HEIC/HEIF format (iPhone), and resizes large images.
    Converts all images to RGB JPEG-compatible format.

    Args:
        image_bytes: Raw image bytes
        filename: Original filename for format detection

    Returns:
        Preprocessed PIL Image in RGB mode (JPEG-compatible)
    """
    # Check if it's a HEIC/HEIF file (iPhone format) by filename or magic bytes
    filename_lower = filename.lower() if filename else ""
    is_heif = filename_lower.endswith((".heic", ".heif"))

    # Also check magic bytes for HEIF format (starts with ftyp followed by heic/mif1/etc)
    if not is_heif and len(image_bytes) > 12:
        # HEIF files have 'ftyp' at offset 4 and 'heic', 'mif1', 'msf1', 'heix' at offset 8
        if image_bytes[4:8] == b"ftyp":
            brand = image_bytes[8:12]
            if brand in (b"heic", b"heix", b"mif1", b"msf1", b"hevc", b"hevx"):
                is_heif = True
                print(f"🍎 Detected HEIF format from magic bytes (brand: {brand.decode('utf-8', errors='ignore')})")

    if is_heif:
        print(f"🍎 Processing iPhone HEIC/HEIF image: {filename}")
        if not HEIC_SUPPORTED:
            raise ValueError("HEIC/HEIF format not supported. Please convert to JPEG before uploading.")

    # Open image (pillow_heif register_heif_opener handles HEIC/HEIF automatically)
    image = Image.open(io.BytesIO(image_bytes))
    print(f"📐 Original: {image.size}, mode: {image.mode}, format: {image.format}")

    # Apply EXIF orientation correction (fixes phone image rotation)
    try:
        transposed = ImageOps.exif_transpose(image)
        if transposed is not None:
            image = transposed
            print("🔄 Applied EXIF orientation correction")
    except Exception as e:
        print(f"⚠️ EXIF transpose failed: {e}")

    # Convert to RGB (handles RGBA, P, L, HEIC modes) - ensures JPEG compatibility
    if image.mode != "RGB":
        print(f"🎨 Converting from {image.mode} to RGB (JPEG-compatible)")
        # For images with transparency, paste on white background
        if image.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = background
        else:
            image = image.convert("RGB")

    # Resize large images for faster processing
    if image.size[0] > MAX_IMAGE_SIZE or image.size[1] > MAX_IMAGE_SIZE:
        original_size = image.size
        image.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.Resampling.LANCZOS)
        print(f"📏 Resized from {original_size} to {image.size}")

    # For HEIF images, re-encode as JPEG to ensure compatibility with model
    if is_heif or image.format in ("HEIF", "HEIC"):
        print("🔄 Converting HEIF to JPEG format for model compatibility")
        jpeg_buffer = io.BytesIO()
        image.save(jpeg_buffer, format="JPEG", quality=95)
        jpeg_buffer.seek(0)
        image = Image.open(jpeg_buffer)
        print(f"✅ Converted to JPEG: {image.size}, mode: {image.mode}")

    return image


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

        # Use safe_load_image for robust image handling (HEIC, EXIF, resizing)
        try:
            image = safe_load_image(image_bytes, file.filename or "")
        except Exception as img_err:
            print(f"❌ Failed to load image: {img_err}")
            return JSONResponse(content={"error": f"Invalid image format: {str(img_err)}"}, status_code=400)

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
