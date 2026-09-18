"""Tests for implied volatility solver."""

import pytest

from packages.options_analytics.pricing.implied_volatility import (
    ImpliedVolatilityError,
    implied_volatility,
)
from packages.options_analytics.schemas import OptionType

# ATM call at 20% vol ≈ 10.45


def test_recover_known_vol():
    iv = implied_volatility(10.45, 100.0, 100.0, 1.0, 0.05, OptionType.CALL)
    assert iv == pytest.approx(0.20, abs=0.01)


def test_zero_price_raises():
    with pytest.raises(ValueError):
        implied_volatility(0.0, 100.0, 100.0, 1.0, 0.05, OptionType.CALL)


def test_price_below_intrinsic_raises():
    # ITM call intrinsic = 10, price = 8 is arbitrage
    with pytest.raises(ImpliedVolatilityError):
        implied_volatility(8.0, 110.0, 100.0, 1.0, 0.05, OptionType.CALL)
