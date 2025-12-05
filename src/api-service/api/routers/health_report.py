from fastapi import APIRouter

from api.utils.utils import get_blob, read_csv_from_gcs, write_csv_to_gcs
from api.utils.health_report_utils import convert_onehot, run_fisher

# Define router
router = APIRouter()


@router.get("/{user_id}")
async def get_health_report(user_id: str):
    """Get health report for a specific user ID"""
    # Read health report CSV from GCS
    pattern = f"data/health_report/health_report_{user_id}.csv"
    blob = get_blob(pattern)
    df = read_csv_from_gcs(blob)

    return df.to_dict(orient="records")


@router.post("/{user_id}")
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

    return {"status": "success", "user_id": user_id, "report_file": report_blob.name}
