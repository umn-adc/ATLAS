"""Option moneyness classification."""

from services.options_analytics.schemas import Moneyness, OptionType

DEFAULT_ATM_TOLERANCE: float = 0.005  # 0.5%


def classify_moneyness(
    spot: float,
    strike: float,
    option_type: OptionType,
    atm_tolerance: float = DEFAULT_ATM_TOLERANCE,
) -> Moneyness:
    """Classify an option as in-the-money, at-the-money, or out-of-the-money.

    ATM if |spot - strike| / strike <= atm_tolerance (default 0.5%).
    For calls: ITM when spot > strike, OTM when spot < strike.
    For puts: ITM when spot < strike, OTM when spot > strike.

    Raises ValueError if spot <= 0, strike <= 0, or atm_tolerance < 0.
    """
    raise NotImplementedError
