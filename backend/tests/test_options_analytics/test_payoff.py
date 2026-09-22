"""Tests for payoff calculations."""

import pytest

from packages.options_analytics.pricing.payoff import call_payoff, put_payoff


def test_call_itm():
    assert call_payoff(110.0, 100.0) == 10.0


def test_call_otm():
    assert call_payoff(90.0, 100.0) == 0.0


def test_put_itm():
    assert put_payoff(90.0, 100.0) == 10.0


def test_put_otm():
    assert put_payoff(110.0, 100.0) == 0.0


@pytest.mark.parametrize(
    "spot, strike",
    [
        (-10.0, 100.0),
        (80.0, -10.0),
        (100.0, 0.0),
    ],
    ids=["spot < 0", "strike < 0", "strike == 0"],
)
def test_invalid_call_payoff(spot, strike):
    with pytest.raises(ValueError):
        call_payoff(spot, strike)


@pytest.mark.parametrize(
    "spot, strike",
    [
        (0.0, 100.0),
        (100.0, 100.0),
    ],
    ids=["spot == 0", "spot == strike"],
)
def test_valid_call_payoff(spot, strike):
    assert call_payoff(spot, strike) == max(spot - strike, 0)


@pytest.mark.parametrize(
    "spot, strike",
    [
        (-10.0, 100.0),
        (80.0, -10.0),
        (100.0, 0.0),
    ],
    ids=["spot < 0", "strike < 0", "strike == 0"],
)
def test_invalid_put_payoff(spot, strike):
    with pytest.raises(ValueError):
        put_payoff(spot, strike)


@pytest.mark.parametrize(
    "spot, strike",
    [
        (0.0, 100.0),
        (100.0, 100.0),
    ],
    ids=["spot == 0", "spot == strike"],
)
def test_valid_put_payoff(spot, strike):
    assert put_payoff(spot, strike) == max(strike - spot, 0)
