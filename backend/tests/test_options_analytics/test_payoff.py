"""Tests for payoff calculations."""

# COMMENTED OUT - Not focus of current sprint
# Uncomment when options_analytics work resumes

# import pytest
#
# from packages.options_analytics.pricing.payoff import call_payoff, put_payoff
#
#
# def test_call_itm():
#     assert call_payoff(110.0, 100.0) == 10.0
#
#
# def test_call_otm():
#     assert call_payoff(90.0, 100.0) == 0.0
#
#
# def test_put_itm():
#     assert put_payoff(90.0, 100.0) == 10.0
#
#
# def test_put_otm():
#     assert put_payoff(110.0, 100.0) == 0.0
#
#
# def test_negative_spot_raises():
#     with pytest.raises(ValueError):
#         call_payoff(-10.0, 100.0)
