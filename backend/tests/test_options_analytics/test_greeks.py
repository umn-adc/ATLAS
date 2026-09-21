"""Tests for Greeks."""

# COMMENTED OUT - Not focus of current sprint
# Uncomment when options_analytics work resumes

# import pytest
#
# from packages.options_analytics.pricing.greeks import delta, gamma, theta, vega
# from packages.options_analytics.schemas import OptionType
#
# S, K, T, r, vol = 100.0, 100.0, 1.0, 0.05, 0.20
#
#
# def test_call_delta_range():
#     d = delta(S, K, T, r, vol, OptionType.CALL)
#     assert 0.5 < d < 0.7
#
#
# def test_put_delta_range():
#     d = delta(S, K, T, r, vol, OptionType.PUT)
#     assert -0.5 > d > -0.7
#
#
# def test_gamma_positive():
#     assert gamma(S, K, T, r, vol) > 0
#
#
# def test_vega_positive():
#     assert vega(S, K, T, r, vol) > 0
#
#
# def test_theta_negative():
#     assert theta(S, K, T, r, vol, OptionType.CALL) < 0
#
#
# def test_invalid_raises():
#     with pytest.raises(ValueError):
#         delta(S, K, T, r, -0.10, OptionType.CALL)
