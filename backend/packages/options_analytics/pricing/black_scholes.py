"""Black-Scholes European option pricing.

Conventions: prices in currency, time in years, vol as decimal (0.20 = 20%), rate as decimal.
"""

import math

from scipy.stats import norm


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
    # Check for valid inputs
    if spot <= 0 or strike <= 0:
        raise ValueError("Spot and Strike must be greater than zero")
    if time_to_expiry < 0:
        raise ValueError("Time to expiry can not be less than zero")
    if volatility < 0:
        raise ValueError("Volatility can not be negative")
    if volatility == 0 and time_to_expiry > 0:
        raise ValueError("Volatility can not be zero when time to expiry is greater than 0")

    if time_to_expiry == 0:
        return max(spot - strike, 0)

    # Black Scholes Calculation
    d1 = (
        math.log(spot / strike) + (risk_free_rate + (math.pow(volatility, 2) / 2)) * time_to_expiry
    ) / (volatility * math.sqrt(time_to_expiry))
    d2 = d1 - (volatility * math.sqrt(time_to_expiry))
    C = float(
        (spot * norm.cdf(d1))
        - (strike * math.exp(-(risk_free_rate * time_to_expiry)) * norm.cdf(d2))
    )
    return C


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
    # Check for valid inputs
    if spot <= 0 or strike <= 0:
        raise ValueError("Spot and Strike must be greater than zero")
    if time_to_expiry < 0:
        raise ValueError("Time to expiry can not be less than zero")
    if volatility < 0:
        raise ValueError("Volatility can not be negative")
    if volatility == 0 and time_to_expiry > 0:
        raise ValueError("Volatility can not be zero when time to expiry is greater than 0")

    if time_to_expiry == 0:
        return max(strike - spot, 0)

    # Black Scholes Calculation
    d1 = (
        math.log(spot / strike) + (risk_free_rate + (math.pow(volatility, 2) / 2)) * time_to_expiry
    ) / (volatility * math.sqrt(time_to_expiry))
    d2 = d1 - (volatility * math.sqrt(time_to_expiry))
    C = float(
        (strike * math.exp(-(risk_free_rate * time_to_expiry)) * norm.cdf(-d2))
        - (spot * norm.cdf(-d1))
    )
    return C


if __name__ == "__main__":
    print(black_scholes_call(100, 100, 30 / 365, 0.045, 0.25))  # Should return $3.04

    print(black_scholes_put(100, 105, 0.5, 0.05, 0.20))  # Should return $6.99
    print(black_scholes_call(100, 105, 0.5, 0.05, 0.20))  # Should return $4.58
    print(black_scholes_put(100, 105, 0, 0.05, 0.20))  # Should return $5
