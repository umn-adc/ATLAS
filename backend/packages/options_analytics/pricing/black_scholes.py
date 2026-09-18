"""Black-Scholes European option pricing.

Conventions: prices in currency, time in years, vol as decimal (0.20 = 20%), rate as decimal.
"""

import math


def _validate(spot: float, strike: float, time_to_expiry: float, volatility: float) -> None:
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if time_to_expiry < 0 or volatility < 0:
        raise ValueError("time to expiry and volatility must be non-negative")
    if time_to_expiry > 0 and volatility == 0:
        raise ValueError("volatility must be positive while time remains")


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def black_scholes_call(
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Return the theoretical price of a European call option using Black-Scholes.

    Formula: C = S·N(d1) - K·e^(-rT)·N(d2)
    At expiry (T=0), returns intrinsic value max(S-K, 0).

    Raises ValueError if spot <= 0, strike <= 0, T < 0, vol < 0, or (vol == 0 and T > 0).
    """
    _validate(spot, strike, time_to_expiry, volatility)
    if time_to_expiry == 0:
        return max(spot - strike, 0.0)
    root_time = math.sqrt(time_to_expiry)
    d1 = (math.log(spot / strike) + (risk_free_rate + volatility**2 / 2) * time_to_expiry) / (volatility * root_time)
    d2 = d1 - volatility * root_time
    return spot * _normal_cdf(d1) - strike * math.exp(-risk_free_rate * time_to_expiry) * _normal_cdf(d2)


def black_scholes_put(
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Return the theoretical price of a European put option using Black-Scholes.

    Formula: P = K·e^(-rT)·N(-d2) - S·N(-d1)
    At expiry (T=0), returns intrinsic value max(K-S, 0).

    Raises ValueError if spot <= 0, strike <= 0, T < 0, vol < 0, or (vol == 0 and T > 0).
    """
    _validate(spot, strike, time_to_expiry, volatility)
    if time_to_expiry == 0:
        return max(strike - spot, 0.0)
    root_time = math.sqrt(time_to_expiry)
    d1 = (math.log(spot / strike) + (risk_free_rate + volatility**2 / 2) * time_to_expiry) / (volatility * root_time)
    d2 = d1 - volatility * root_time
    discount = math.exp(-risk_free_rate * time_to_expiry)
    return strike * discount * _normal_cdf(-d2) - spot * _normal_cdf(-d1)
