"""Option payoff at expiration."""


def call_payoff(spot: float, strike: float) -> float:
    """Return max(spot - strike, 0) — the profit from exercising a call at expiration.

    Raises ValueError if spot < 0 or strike <= 0.
    """
    if spot < 0 or strike <= 0:
        raise ValueError("Spot price must be >= 0 and strike price must be > 0.")
    return max(spot - strike, 0)


def put_payoff(spot: float, strike: float) -> float:
    """Return max(strike - spot, 0) — the profit from exercising a put at expiration.

    Raises ValueError if spot < 0 or strike <= 0.
    """
    if spot < 0 or strike <= 0:
        raise ValueError("Spot price must be >= 0 and strike price must be > 0.")
    return max(strike - spot, 0)
