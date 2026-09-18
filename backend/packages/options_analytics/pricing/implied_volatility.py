"""Implied volatility solver."""

from services.options_analytics.schemas import OptionType


class ImpliedVolatilityError(Exception):
    """Raised when IV cannot be computed (arbitrage price, no convergence, etc)."""


def implied_volatility(
    observed_price: float,
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    option_type: OptionType,
    max_iterations: int = 100,
    tolerance: float = 1e-6,
) -> float:
    """Find the volatility that makes Black-Scholes price equal the observed market price.

    Returns volatility as a decimal (0.20 = 20%).
    Raises ValueError if price <= 0, spot <= 0, strike <= 0, or T <= 0.
    Raises ImpliedVolatilityError if price is below intrinsic or solver doesn't converge.
    """
    raise NotImplementedError
