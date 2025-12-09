"""
Health report APIs
"""

import math
import pandas as pd
from fastapi import APIRouter, HTTPException

from api.utils.utils import get_gcs_bucket, get_blob, read_csv_from_gcs, write_csv_to_gcs
from api.utils.health_report_utils import convert_onehot, run_fisher

# Define router
router = APIRouter()


@router.post("/{user_id}")
async def create_health_report(user_id: str):
    """Create empty health report for a new user ID, only if it does not exist"""
    # Construct the GCS path
    bucket = get_gcs_bucket()
    path = f"data/health_report/health_report_{user_id}.csv"
    blob = bucket.blob(path)

    # Check if the file already exists
    if blob.exists():
        raise HTTPException(status_code=409, detail=f"Health report for user {user_id} already exists.")

    # Create empty DataFrame
    columns = ["metric", "value", "odds_ratio", "p_value", "p_value_adj", "significant"]
    df = pd.DataFrame(columns=columns)

    # Write empty health report CSV to GCS
    write_csv_to_gcs(blob, df)

    return {"status": "success", "user_id": user_id, "file": blob.name}


@router.get("/{user_id}")
async def get_health_report(user_id: str):
    """Get health report for a specific user ID"""
    # Read health report CSV from GCS
    pattern = f"data/health_report/health_report_{user_id}.csv"
    blob = get_blob(pattern)
    df = read_csv_from_gcs(blob)

    # Convert to dict and handle NaN/Inf values
    records = df.to_dict(orient="records")
    for record in records:
        for key, value in record.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                record[key] = None

    return records


@router.put("/{user_id}")
async def update_health_report(user_id: str):
    """Update health report for a specific user ID"""
    # Read meal history CSV from GCS
    history_pattern = f"data/meal_history/meal_history_{user_id}.csv"
    history_blob = get_blob(history_pattern)
    history_df = read_csv_from_gcs(history_blob)

    # Convert to one-hot encoding
    history_df = convert_onehot(history_df)

    # Run Fisher's exact test
    report_df = run_fisher(history_df)

    # Write health report CSV to GCS
    report_pattern = f"data/health_report/health_report_{user_id}.csv"
    report_blob = get_blob(report_pattern)
    write_csv_to_gcs(report_blob, report_df)

    return {"status": "success", "user_id": user_id, "file": report_blob.name}
