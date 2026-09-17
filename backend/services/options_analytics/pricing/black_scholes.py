"""Black-Scholes European option pricing.

Conventions: prices in currency, time in years, vol as decimal (0.20 = 20%), rate as decimal.
"""


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
    raise NotImplementedError


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
    raise NotImplementedError
