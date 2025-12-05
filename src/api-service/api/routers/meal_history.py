"""
Meal history APIs
"""

import pandas as pd
from fastapi import APIRouter

from api.utils.utils import get_blob, read_csv_from_gcs, write_csv_to_gcs


# Define router
router = APIRouter()


@router.get("/{user_id}")
async def get_meal_history(user_id: str):
    """Get meal history for a specific user ID"""
    # Read meal history CSV from GCS
    pattern = f"data/meal_history/meal_history_{user_id}.csv"
    blob = get_blob(pattern)
    df = read_csv_from_gcs(blob)

    return df.to_dict(orient="records")


@router.post("/{user_id}")
async def update_meal_history(meal: dict, user_id: str):
    """Update meal history for a specific user ID"""
    # Read meal history CSV from GCS
    pattern = f"data/meal_history/meal_history_{user_id}.csv"
    blob = get_blob(pattern)
    df = read_csv_from_gcs(blob)

    # Prepare new row
    new_row = {
        "date_time": meal.get("date_time"),
        "ingredients": meal.get("ingredients", ""),
        "symptoms": meal.get("symptoms", ""),
    }

    # Append new row
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Write CSV to GCS
    write_csv_to_gcs(blob, df)

    return {"status": "success", "user_id": user_id, "file": blob.name}
