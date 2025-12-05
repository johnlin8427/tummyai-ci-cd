import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests


def convert_onehot(history: pd.DataFrame) -> list[str]:
    """
    One-hot encode ingredients and symptoms in the meal history DataFrame.

    Parameters:
        history : pd.DataFrame
            DataFrame with columns "ingredients" and "symptoms" containing
            comma-separated strings.

    Returns:
        pd.DataFrame
            DataFrame with one-hot encoded columns for each ingredient and symptom.
    """
    try:
        # Fill NaN as ""
        # Convert comma-separated strings into lists
        # Remove any leading/trailing whitespace from each item
        for col in ["ingredients", "symptoms"]:
            history[col] = history[col].fillna("")
            history[col] = history[col].apply(lambda x: x.split(",") if x else [])
            history[col] = history[col].apply(lambda lst: [i.strip() for i in lst])

        # Get all unique ingredients and sort alphabetically
        ingredient_cols = sorted({ing for sublist in history["ingredients"] for ing in sublist})
        symptom_cols = sorted({sym for sublist in history["symptoms"] for sym in sublist})

        # Create one-hot columns for ingredients
        for ing in ingredient_cols:
            history[f"ingredient_{ing}"] = history["ingredients"].apply(lambda x: 1 if ing in x else 0)

        # Create one-hot columns for symptoms
        for sym in symptom_cols:
            history[f"symptom_{sym}"] = history["symptoms"].apply(lambda x: 1 if sym in x else 0)

        # Drop the original list columns
        history = history.drop(columns=["ingredients", "symptoms"])
        return history
    except Exception as e:
        print(f"Error in one-hot encoding: {str(e)}")
        return []


def run_fisher(history: pd.DataFrame) -> pd.DataFrame:
    """
    Run Fisher's exact test.

    Parameters:
        history : pd.DataFrame
            One-hot encoded DataFrame with columns for ingredients and symptoms (values 0/1)

    Returns:
        pd.DataFrame
            DataFrame with columns: symptom, ingredient, odds_ratio, p_value, p_value_adj, significant
    """
    # Define ingredients
    ingredients = [c.replace("ingredient_", "") for c in history.columns if c.startswith("ingredient_")]

    # Define symptoms
    symptoms = [c.replace("symptom_", "") for c in history.columns if c.startswith("symptom_")]

    results = []
    for symptom in symptoms:
        symptom_col = f"symptom_{symptom}"
        if symptom_col not in history.columns:
            continue

        for ingredient in ingredients:
            # Build 2x2 contingency table
            table = pd.crosstab(history[f"ingredient_{ingredient}"], history[f"symptom_{symptom}"])

            # Ensure table is 2x2
            if table.shape != (2, 2):
                # Add missing row/column if needed
                table = table.reindex(index=[0, 1], columns=[0, 1], fill_value=0)

            # Perform Fisher's exact test
            odds_ratio, p_value = fisher_exact(table)

            # Append to results
            results.append({"symptom": symptom, "ingredient": ingredient, "odds_ratio": odds_ratio, "p_value": p_value})

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Multiple hypotheses testing correction (Benjamini-Hochberg)
    reject, pvals_corrected, _, _ = multipletests(results_df["p_value"].values, alpha=0.05, method="fdr_bh")
    results_df["p_value_adj"] = pvals_corrected
    results_df["significant"] = reject

    return results_df
