"""Shared types for options pricing."""

from enum import Enum


class OptionType(str, Enum):
    """Call or put."""

    CALL = "call"
    PUT = "put"


class Moneyness(str, Enum):
    """ITM, ATM, or OTM. ATM tolerance: 0.5% of strike."""

    ITM = "itm"
    ATM = "atm"
    OTM = "otm"
