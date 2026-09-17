"""Tests for moneyness classification."""

import pytest

from services.options_analytics.pricing.moneyness import classify_moneyness
from services.options_analytics.schemas import Moneyness, OptionType


def test_call_itm():
    assert classify_moneyness(110.0, 100.0, OptionType.CALL) == Moneyness.ITM


def test_call_otm():
    assert classify_moneyness(90.0, 100.0, OptionType.CALL) == Moneyness.OTM


def test_call_atm():
    assert classify_moneyness(100.0, 100.0, OptionType.CALL) == Moneyness.ATM


def test_put_itm():
    assert classify_moneyness(90.0, 100.0, OptionType.PUT) == Moneyness.ITM


def test_put_otm():
    assert classify_moneyness(110.0, 100.0, OptionType.PUT) == Moneyness.OTM


def test_invalid_raises():
    with pytest.raises(ValueError):
        classify_moneyness(-10.0, 100.0, OptionType.CALL)
