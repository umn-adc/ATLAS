"""Tests for Black-Scholes pricing."""

import math

import pytest

from services.options_analytics.pricing.black_scholes import black_scholes_call, black_scholes_put

# ATM: S=100, K=100, T=1, r=0.05, σ=0.20 → Call≈10.45, Put≈5.57


def test_atm_call():
    assert black_scholes_call(100.0, 100.0, 1.0, 0.05, 0.20) == pytest.approx(10.45, abs=0.1)


def test_atm_put():
    assert black_scholes_put(100.0, 100.0, 1.0, 0.05, 0.20) == pytest.approx(5.57, abs=0.1)


def test_put_call_parity():
    S, K, T, r, vol = 100.0, 100.0, 1.0, 0.05, 0.20
    call = black_scholes_call(S, K, T, r, vol)
    put = black_scholes_put(S, K, T, r, vol)
    assert call - put == pytest.approx(S - K * math.exp(-r * T), abs=0.01)


def test_invalid_raises():
    with pytest.raises(ValueError):
        black_scholes_call(-100.0, 100.0, 1.0, 0.05, 0.20)
