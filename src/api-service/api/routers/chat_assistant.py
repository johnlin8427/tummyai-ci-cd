"""
Chat Assistant API using LLM
"""

from fastapi import APIRouter, HTTPException
from google.genai import types

from api.utils.utils import get_blob, read_csv_from_gcs
from api.utils.chat_assistant_utils import get_gemini_client, create_chat_prompt


# Define router
router = APIRouter()

# Initialize Gemini client at startup
client = get_gemini_client()


@router.get("/{user_id}")
async def get_recommendations(user_id: str):
    """Generate personalized dietary recommendations for a user based on their meal history and health report"""

    try:
        # Fetch meal history
        meal_history_pattern = f"data/meal_history/meal_history_{user_id}.csv"
        meal_history_blob = get_blob(meal_history_pattern)
        meal_history_df = read_csv_from_gcs(meal_history_blob)

        # Fetch health report
        health_report_pattern = f"data/health_report/health_report_{user_id}.csv"
        health_report_blob = get_blob(health_report_pattern)
        health_report_df = read_csv_from_gcs(health_report_blob)

        # Filter health report to show only relevant correlations (p_value < 0.2, odds_ratio > 1 or null)
        filtered_health_report_df = health_report_df[
            ((health_report_df["odds_ratio"].isna()) | (health_report_df["odds_ratio"] > 1))
            & (health_report_df["p_value"] < 0.2)
        ]

        # Convert dataframes to readable format
        meal_history_text = meal_history_df.to_string(index=False)
        health_report_text = (
            filtered_health_report_df.to_string(index=False)
            if not filtered_health_report_df.empty
            else "No significant food-symptom correlations found."
        )

        # Create the prompt
        prompt = create_chat_prompt(meal_history_text, health_report_text)

        # Call Gemini API
        recommendations_text = None
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=300,
            ),
        )
        recommendations_text = response.text

        return {
            "recommendations": recommendations_text,
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Data not found for user {user_id}.")
