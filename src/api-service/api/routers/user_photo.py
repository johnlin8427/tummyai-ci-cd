"""
User photo APIs
"""

import io
from datetime import datetime
from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse

from api.utils.utils import get_gcs_bucket


# Define router
router = APIRouter()


@router.post("/{user_id}/{date_time}")
async def upload_user_photo(user_id: str, date_time: str, file: UploadFile = File(...)):
    """Upload user photo for a specific user ID and date_time"""
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Generate unique filename with user date_time
    # Convert date_time to filename-safe format (remove spaces and colons)
    timestamp = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S").isoformat()
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    file_name = f"user_photo_{user_id}_{timestamp}.{file_extension}"

    # Construct the GCS path
    bucket = get_gcs_bucket()
    path = f"data/user_photo/{file_name}"
    blob = bucket.blob(path)

    # Read file content and upload to GCS
    content = await file.read()
    blob.upload_from_string(content, content_type=file.content_type)

    return {"status": "success", "user_id": user_id, "date_time": date_time, "file": blob.name}


@router.get("/{user_id}/{date_time}")
async def get_user_photo(user_id: str, date_time: str):
    """Get meal photo for a specific user ID and date_time"""
    # Convert date_time to filename format
    timestamp = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S").isoformat()

    # Try common image extensions
    bucket = get_gcs_bucket()
    extensions = ["jpg", "jpeg", "png", "gif", "webp"]

    blob = None
    found_extension = None
    for ext in extensions:
        file_name = f"user_photo_{user_id}_{timestamp}.{ext}"
        path = f"data/user_photo/{file_name}"
        temp_blob = bucket.blob(path)
        if temp_blob.exists():
            blob = temp_blob
            found_extension = ext
            break

    if not blob:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Download photo content
    photo_bytes = blob.download_as_bytes()

    # Return as streaming response
    return StreamingResponse(
        io.BytesIO(photo_bytes),
        media_type=blob.content_type or "image/jpeg",
        headers={"Content-Disposition": f'inline; filename="meal_{user_id}_{timestamp}.{found_extension}"'},
    )
