"""
User list APIs
"""

from fastapi import APIRouter, HTTPException

from api.utils.utils import get_gcs_bucket


# Define router
router = APIRouter()


@router.get("/")
async def get_user_list():
    """Get user list from GCS bucket"""
    try:
        bucket = get_gcs_bucket()
        pattern = "data/reference/user_list.txt"
        blob = bucket.blob(pattern)

        if not blob.exists():
            raise HTTPException(status_code=404, detail="User list not found")

        content = blob.download_as_text()
        user_list = [line.strip() for line in content.split("\n") if line.strip()]

        return {"user_list": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user list: {str(e)}")


@router.put("/{user_id}")
async def add_user(user_id: str):
    """Add a new user to the user list"""
    try:
        bucket = get_gcs_bucket()
        pattern = "data/reference/user_list.txt"
        blob = bucket.blob(pattern)

        if not blob.exists():
            raise HTTPException(status_code=404, detail="User list not found")

        content = blob.download_as_text()
        user_list = [line.strip() for line in content.split("\n") if line.strip()]

        # Add new user
        if user_id not in user_list:
            user_list.append(user_id)

            # Write updated list back to GCS
            blob.upload_from_string("\n".join(user_list), content_type="text/plain")
            return {"status": "success", "message": f"User {user_id} added", "user_list": user_list}
        else:
            return {"status": "exists", "message": f"User {user_id} already exists", "user_list": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user list: {str(e)}")


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user and all associated data from GCS bucket"""
    try:
        bucket = get_gcs_bucket()
        deleted_items = []

        # Remove user from user list
        pattern = "data/reference/user_list.txt"
        user_list_blob = bucket.blob(pattern)

        if not user_list_blob.exists():
            raise HTTPException(status_code=404, detail="User list not found")

        content = user_list_blob.download_as_text()
        user_list = [line.strip() for line in content.split("\n") if line.strip()]

        if user_id in user_list:
            user_list.remove(user_id)
            user_list_blob.upload_from_string("\n".join(user_list), content_type="text/plain")
            deleted_items.append("user list entry")
        else:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found in user list")

        # Delete meal history file
        meal_history_path = f"data/meal_history/meal_history_{user_id}.csv"
        meal_history_blob = bucket.blob(meal_history_path)
        if meal_history_blob.exists():
            meal_history_blob.delete()
            deleted_items.append("meal history")

        # Delete health report file
        health_report_path = f"data/health_report/health_report_{user_id}.csv"
        health_report_blob = bucket.blob(health_report_path)
        if health_report_blob.exists():
            health_report_blob.delete()
            deleted_items.append("health report")

        # Delete all user photos
        photo_prefix = f"data/user_photo/user_photo_{user_id}_"
        photo_blobs = list(bucket.list_blobs(prefix=photo_prefix))

        photo_count = 0
        for photo_blob in photo_blobs:
            photo_blob.delete()
            photo_count += 1

        if photo_count > 0:
            deleted_items.append(f"{photo_count} photo(s)")

        return {
            "status": "success",
            "message": f"Deleted user {user_id} and all associated data",
            "deleted_items": deleted_items,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
