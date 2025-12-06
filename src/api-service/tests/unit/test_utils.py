"""
Unit tests for utils module
"""

import pytest
from api.utils.utils import power


class TestPower:
    """Tests for the power function"""

    def test_power_positive_integers(self):
        """Test power with positive integers"""
        assert power(2, 3) == 8
        assert power(3, 2) == 9
        assert power(5, 2) == 25
        assert power(10, 2) == 100

    def test_power_with_zero_exponent(self):
        """Test power with zero exponent (any number^0 = 1)"""
        assert power(5, 0) == 1
        assert power(100, 0) == 1
        assert power(0, 0) == 1

    def test_power_with_one(self):
        """Test power with base or exponent of one"""
        assert power(1, 5) == 1
        assert power(5, 1) == 5
        assert power(1, 1) == 1

    def test_power_negative_base(self):
        """Test power with negative base"""
        assert power(-2, 2) == 4
        assert power(-3, 3) == -27
        assert power(-2, 4) == 16
        assert power(-5, 2) == 25

    def test_power_negative_exponent(self):
        """Test power with negative exponent (1/base^exp)"""
        assert power(2, -1) == pytest.approx(0.5)
        assert power(2, -2) == pytest.approx(0.25)
        assert power(10, -1) == pytest.approx(0.1)

    def test_power_with_floats(self):
        """Test power with floating point numbers"""
        assert power(2.5, 2) == pytest.approx(6.25)
        assert power(1.5, 3) == pytest.approx(3.375)
        assert power(0.5, 2) == pytest.approx(0.25)

    def test_power_large_numbers(self):
        """Test power with large numbers"""
        assert power(10, 6) == 1000000
        assert power(2, 10) == 1024

    def test_power_fractional_exponent(self):
        """Test power with fractional exponent (roots)"""
        assert power(4, 0.5) == pytest.approx(2.0)  # square root
        assert power(8, 1 / 3) == pytest.approx(2.0)  # cube root
        assert power(16, 0.25) == pytest.approx(2.0)  # fourth root

    def test_power_special_float_values(self):
        """Test special float values"""
        import math

        assert math.isnan(power(float("nan"), 2))
        assert power(float("inf"), 2) == float("inf")
        assert power(2, float("inf")) == float("inf")

    def test_power_invalid_inputs(self):
        """Test that invalid inputs raise TypeError"""
        with pytest.raises(TypeError):
            power("3", 4)
        with pytest.raises(TypeError):
            power(3, "4")
        with pytest.raises(TypeError):
            power(None, 4)
        with pytest.raises(TypeError):
            power(3, None)
        with pytest.raises(TypeError):
            power([3], 4)
        with pytest.raises(TypeError):
            power(3, [4])
        with pytest.raises(TypeError):
            power({}, 4)

    def test_power_boolean_values(self):
        """Test with boolean values (True=1, False=0)"""
        assert power(True, 5) == 1
        assert power(False, 5) == 0
        assert power(2, True) == 2
