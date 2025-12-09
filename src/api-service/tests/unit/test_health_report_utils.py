"""
Unit tests for health_report utilities module
Tests the one-hot encoding and Fisher's exact test functions
"""
import pytest
import pandas as pd
import numpy as np

from api.utils.health_report_utils import convert_onehot, run_fisher


class TestConvertOnehot:
    """Tests for the convert_onehot() function"""

    def test_convert_onehot_simple(self):
        """Test convert_onehot with simple input"""
        data = {
            "ingredients": ["milk, cheese", "cheese"],
            "symptoms": ["nausea", "headache, nausea"],
        }
        history = pd.DataFrame(data)
        onehot_df = convert_onehot(history)

        expected_columns = sorted(
            [
                "ingredient_cheese",
                "ingredient_milk",
                "symptom_headache",
                "symptom_nausea",
            ]
        )
        assert sorted(onehot_df.columns.tolist()) == expected_columns

        assert onehot_df.iloc[0]["ingredient_cheese"] == 1
        assert onehot_df.iloc[0]["ingredient_milk"] == 1
        assert onehot_df.iloc[0]["symptom_headache"] == 0
        assert onehot_df.iloc[0]["symptom_nausea"] == 1

        assert onehot_df.iloc[1]["ingredient_cheese"] == 1
        assert onehot_df.iloc[1]["ingredient_milk"] == 0
        assert onehot_df.iloc[1]["symptom_headache"] == 1
        assert onehot_df.iloc[1]["symptom_nausea"] == 1

    def test_convert_onehot_empty(self):
        """Test convert_onehot with empty input"""
        history = pd.DataFrame({"ingredients": [], "symptoms": []})
        onehot_df = convert_onehot(history)
        assert onehot_df.empty

    def test_convert_onehot_with_dates(self):
        """Test convert_onehot preserves date_time column"""
        history = pd.DataFrame(
            {
                "date_time": ["2025-11-25 08:00:00", "2025-11-25 09:00:00", "2025-11-25 10:00:00"],
                "ingredients": ["sugar, milk", "milk, cocoa", None],
                "symptoms": ["headache, nausea", None, "fatigue"],
            }
        )
        history_onehot = convert_onehot(history)

        # Should have date_time column preserved
        assert "date_time" in history_onehot.columns

        # Check ingredient columns
        assert "ingredient_cocoa" in history_onehot.columns
        assert "ingredient_milk" in history_onehot.columns
        assert "ingredient_sugar" in history_onehot.columns

        # Check symptom columns
        assert "symptom_fatigue" in history_onehot.columns
        assert "symptom_headache" in history_onehot.columns
        assert "symptom_nausea" in history_onehot.columns

    def test_convert_onehot_handles_none(self):
        """Test convert_onehot handles None/NaN values"""
        history = pd.DataFrame(
            {
                "ingredients": ["milk", None, "cheese"],
                "symptoms": [None, "headache", "nausea"],
            }
        )
        onehot_df = convert_onehot(history)

        # Should not raise error
        assert not onehot_df.empty
        assert "ingredient_milk" in onehot_df.columns
        assert "ingredient_cheese" in onehot_df.columns

    def test_convert_onehot_trims_whitespace(self):
        """Test convert_onehot trims whitespace from ingredients/symptoms"""
        history = pd.DataFrame(
            {
                "ingredients": ["  milk  , cheese  "],
                "symptoms": ["  headache  "],
            }
        )
        onehot_df = convert_onehot(history)

        # Should trim whitespace
        assert "ingredient_milk" in onehot_df.columns
        assert "ingredient_cheese" in onehot_df.columns
        assert "symptom_headache" in onehot_df.columns


class TestRunFisher:
    """Tests for the run_fisher() function"""

    def test_run_fisher_simple(self):
        """Test run_fisher with simple input"""
        data = {
            "ingredient_cheese": [1, 1, 0, 0],
            "ingredient_milk": [1, 0, 1, 0],
            "symptom_nausea": [1, 0, 1, 0],
        }
        history = pd.DataFrame(data)
        results_df = run_fisher(history)

        assert not results_df.empty
        expected_columns = {
            "symptom": str,
            "ingredient": str,
            "odds_ratio": float,
            "p_value": float,
            "p_value_adj": float,
            "significant": np.bool_,
        }
        for col, col_type in expected_columns.items():
            assert col in results_df.columns
            assert isinstance(results_df[col].iloc[0], col_type)

    def test_run_fisher_empty(self):
        """Test run_fisher with empty input"""
        history = pd.DataFrame()
        results_df = run_fisher(history)
        assert results_df.empty

    def test_run_fisher_returns_dataframe(self):
        """Test run_fisher returns a DataFrame"""
        history_onehot = pd.DataFrame(
            {
                "date_time": ["2025-11-25 08:00:00", "2025-11-25 09:00:00", "2025-11-25 10:00:00"],
                "ingredient_cocoa": [0, 1, 0],
                "ingredient_milk": [1, 1, 0],
                "ingredient_sugar": [1, 0, 0],
                "symptom_cramping": [0, 0, 1],
                "symptom_bloating": [1, 0, 0],
                "symptom_diarrhea": [1, 0, 0],
                "symptom_nausea": [1, 0, 0],
            }
        )
        fisher_df = run_fisher(history_onehot)
        assert isinstance(fisher_df, pd.DataFrame)

    def test_run_fisher_includes_all_combinations(self):
        """Test run_fisher tests all ingredient-symptom combinations"""
        history = pd.DataFrame(
            {
                "ingredient_a": [1, 0, 1, 0],
                "ingredient_b": [0, 1, 0, 1],
                "symptom_x": [1, 0, 0, 1],
                "symptom_y": [0, 1, 1, 0],
            }
        )
        results_df = run_fisher(history)

        # Should have 2 ingredients x 2 symptoms = 4 combinations
        assert len(results_df) == 4

    def test_run_fisher_significant_column(self):
        """Test run_fisher includes significance after multiple testing correction"""
        history = pd.DataFrame(
            {
                "ingredient_milk": [1, 1, 1, 0, 0, 0],
                "ingredient_cheese": [0, 0, 0, 1, 1, 1],
                "symptom_nausea": [1, 1, 1, 0, 0, 0],
            }
        )
        results_df = run_fisher(history)

        assert "significant" in results_df.columns
        assert "p_value_adj" in results_df.columns

    def test_run_fisher_handles_missing_values(self):
        """Test run_fisher handles sparse tables"""
        history = pd.DataFrame(
            {
                "ingredient_rare": [1, 0, 0, 0, 0, 0],
                "symptom_common": [1, 1, 1, 1, 1, 0],
            }
        )
        results_df = run_fisher(history)

        # Should handle 2x2 table with some zero cells
        assert not results_df.empty


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
