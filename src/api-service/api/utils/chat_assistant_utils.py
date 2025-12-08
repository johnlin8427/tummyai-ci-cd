"""
Utility functions for chat assistant
"""

from google import genai
from google.auth import default
from google.auth.transport.requests import Request


def get_gemini_client():
    """Initialize Gemini client with GCP service account authentication"""
    try:
        # Get credentials from the environment (uses GOOGLE_APPLICATION_CREDENTIALS)
        credentials, project = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

        # Refresh the credentials to get an access token
        if not credentials.valid:
            credentials.refresh(Request())

        # Initialize Gemini client with the credentials
        client = genai.Client(vertexai=True, project=project, location="us-central1")
        return client
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None


def create_chat_prompt(meal_history_text: str, health_report_text: str) -> str:
    """Create the prompt for generating personalized dietary recommendations

    Args:
        meal_history_text: String representation of the user's meal history
        health_report_text: String representation of the user's health report

    Returns:
        Formatted prompt for the LLM
    """
    prompt = f"""
    You are a board-certified gastroenterologist specializing in Irritable Bowel Syndrome (IBS).
    You are reviewing data for a patient with IBS who has been tracking their meals and symptoms.

    ## Patient Data Summary

    ### Recent Meal History
    {meal_history_text}

    ### Statistical Health Report
    {health_report_text}

    **Statistical Interpretation Guide:**
    - odds_ratio > 1 or null: Ingredient is associated with increased symptom occurrence
    - p_value_adj < 0.05: Statistically significant correlation (high confidence)
    - p_value_adj 0.05-0.2: Moderate evidence of correlation

    ## Your Task

    Based on this data, provide 4 concise, actionable dietary recommendations for this IBS patient.

    **Critical Requirements:**
    1. Format as a bullet list with each bullet on a single line (max 100 characters per line)
    2. Start each bullet with a bullet point character (•)
    3. Focus on the most important trigger foods found in the data
    4. Be specific and actionable
    5. Use a compassionate, professional tone

    **Example Format:**
    • Avoid [specific ingredient] which shows strong correlation with [symptom]
    • Try [low-FODMAP alternative] instead of [trigger food]
    • Continue tracking meals to refine your personalized diet plan

    Provide ONLY the bullet points, nothing else. Each bullet should be complete but concise.
    """

    return prompt
