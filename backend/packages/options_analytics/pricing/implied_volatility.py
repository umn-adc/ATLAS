"""Implied volatility solver."""
import math 

from packages.options_analytics.schemas import OptionType
from greeks import vega
from black_scholes import black_scholes_call, black_scholes_put


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
    vega = Newton-Raphson derivative
    """
    if observed_price <= 0:
        raise ValueError("")
    if spot <= 0:
        raise ValueError("")
    if strike <= 0:
        raise ValueError("")
    if time_to_expiry <=0:
        raise ValueError("")

    is_call = option_type == OptionType.CALL

    discounted_strike = strike * math.exp(-risk_free_rate * time_to_expiry)
    if is_call:
        intrinsic = max(spot - discounted_strike, 0.0)
    else:
        intrinsic = max(discounted_strike - spot, 0.0)
    if observed_price < intrinsic:
        raise ImpliedVolatilityError("Price is below intrinsic value (arbitrage)")

    price_function = black_scholes_call if is_call else black_scholes_put

    volatility = 0.2

    for _ in range(max_iterations):
        price = price_function(spot, strike, time_to_expiry, risk_free_rate, volatility)
        diff = price - observed_price
        if abs(diff) <= tolerance:
            return volatility

        v = vega(spot, strike, time_to_expiry, risk_free_rate, volatility) * 100
        if v <= 1e-10:
            raise ImpliedVolatilityError("Vega too small; colver cannot converge")

        volatility -= diff / v
        if volatility <= 0:
            raise ImpliedVolatilityError("Solver stepped to non-positive volatility")
    
    raise ImpliedVolatilityError("IV did not converge")
