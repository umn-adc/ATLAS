"""Option Greeks. They are the sensitivities of option price to market factors.

Conventions: prices in currency, time in years, vol as decimal (0.20 = 20%).
"""

from packages.options_analytics.schemas import OptionType


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError
