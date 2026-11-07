"""Option Greeks. They are the sensitivities of option price to market factors.

Conventions: prices in currency, time in years, vol as decimal (0.20 = 20%).
"""

import math

from scipy.stats import norm

from packages.options_analytics.schemas import OptionType


def _d1_d2(
    spot: float, strike: float, time_to_expiry: float, risk_free_rate: float, volatility: float
) -> tuple[float, float]:
    vol_sqrt_t = volatility * math.sqrt(time_to_expiry)
    drift = risk_free_rate + 0.5 * (volatility**2) * time_to_expiry

    d1 = (
        math.log(spot / strike) + ((risk_free_rate + 0.5 * (volatility**2)) * time_to_expiry)
    ) / vol_sqrt_t

    return d1, d1 - vol_sqrt_t


def delta(
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
    option_type: OptionType,
) -> float:
    """Return how much the option price changes per $1 move in the underlying.

    Call delta is in [0, 1], put delta is in [-1, 0].
    Raises ValueError if inputs are invalid.
    """
    if spot < 0 or strike <= 0 or volatility <= 0 or time_to_expiry <= 0:
        raise ValueError("Invalid inputs.")

    d1, _ = _d1_d2(spot, strike, time_to_expiry, risk_free_rate, volatility)

    if option_type == OptionType.CALL:
        return float(norm.cdf(d1))
    elif option_type == OptionType.PUT:
        return float(norm.cdf(d1) - 1.0)
    else:
        raise ValueError("Invalid option type.")


def gamma(
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Return how much delta changes per $1 move in the underlying asset.

    Same for calls and puts. Always non-negative, highest for ATM near expiry.
    Raises ValueError if T <= 0 or vol <= 0.
    """
    if time_to_expiry <= 0 or volatility <= 0:
        raise ValueError("Time to expiry must be > 0 and volatility must be > 0")

    d1, _ = _d1_d2(spot, strike, time_to_expiry, risk_free_rate, volatility)

    return float(norm.pdf(d1) / (spot * volatility * math.sqrt(time_to_expiry)))


def vega(
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Return how much the option price changes per 1% increase in volatility.

    Same for calls and puts. Returns 0 at expiry.
    Raises ValueError if inputs are invalid.
    """
    if spot < 0 or strike <= 0 or volatility <= 0:
        raise ValueError("Invalid inputs.")

    d1, _ = _d1_d2(spot, strike, time_to_expiry, risk_free_rate, volatility)

    return float(spot * norm.pdf(d1) * math.sqrt(time_to_expiry))


def theta(
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
    option_type: OptionType,
) -> float:
    """Return the daily time decay — how much value the option loses per day.

    Usually negative (options lose value over time).
    Raises ValueError if T <= 0.
    """
    if time_to_expiry <= 0:
        raise ValueError("Time to expiry must be > 0")

    d1, d2 = _d1_d2(spot, strike, time_to_expiry, risk_free_rate, volatility)

    decay = -spot * norm.pdf(d1) * volatility / (2 * math.sqrt(volatility))
    disc = risk_free_rate * strike * math.exp(-risk_free_rate * time_to_expiry)

    call = decay - disc * norm.cdf(d2)
    put = decay + disc * norm.cdf(-d2)

    if option_type == OptionType.CALL:
        return float(call)
    elif option_type == OptionType.PUT:
        return float(put)
    else:
        raise ValueError("Invalid option type.")
