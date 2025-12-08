"""
Meal history APIs
"""

import pandas as pd
from fastapi import APIRouter, HTTPException

from api.utils.utils import get_gcs_bucket, get_blob, read_csv_from_gcs, write_csv_to_gcs


# Define router
router = APIRouter()


@router.post("/{user_id}")
async def create_meal_history(user_id: str):
    """Create empty meal history for a new user ID, only if it does not exist"""
    # Construct the GCS path
    bucket = get_gcs_bucket()
    path = f"data/meal_history/meal_history_{user_id}.csv"
    blob = bucket.blob(path)

    # Check if the file already exists
    if blob.exists():
        raise HTTPException(status_code=409, detail=f"Meal history for user {user_id} already exists.")

    # Create empty DataFrame
    columns = ["date_time", "dish", "ingredients", "symptoms"]
    df = pd.DataFrame(columns=columns)

    # Write empty meal history CSV to GCS
    write_csv_to_gcs(blob, df)

    return {"status": "success", "user_id": user_id, "file": blob.name}


@router.get("/{user_id}")
async def get_meal_history(user_id: str):
    """Get meal history for a specific user ID"""
    # Read meal history CSV from GCS
    pattern = f"data/meal_history/meal_history_{user_id}.csv"
    blob = get_blob(pattern)
    df = read_csv_from_gcs(blob)

    return df.to_dict(orient="records")


@router.put("/{user_id}")
async def update_meal_history(meal: dict, user_id: str):
    """Update meal history for a specific user ID"""
    # Read meal history CSV from GCS
    pattern = f"data/meal_history/meal_history_{user_id}.csv"
    blob = get_blob(pattern)
    df = read_csv_from_gcs(blob)

    # Prepare new row
    new_row = {
        "date_time": meal.get("date_time"),
        "dish": meal.get("dish", ""),
        "ingredients": meal.get("ingredients", ""),
        "symptoms": meal.get("symptoms", ""),
    }

    # Append new row
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Write CSV to GCS
    write_csv_to_gcs(blob, df)

    return {"status": "success", "user_id": user_id, "file": blob.name}
