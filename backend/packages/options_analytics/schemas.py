"""Shared data contracts for the ATLAS options pricing service."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OptionType(str, Enum):
    """Supported option types."""

    CALL = "call"
    PUT = "put"


class Moneyness(str, Enum):
    """Classification relative to an option's strike."""

    ITM = "ITM"
    ATM = "ATM"
    OTM = "OTM"


class OptionContract(BaseModel):
    """Identify a European option contract.

    Attributes:
        symbol: Unique option contract identifier.
        underlying_symbol: Symbol of the underlying asset.
        strike: Strike price in currency units.
        expiration: Option expiration timestamp in UTC.
        option_type: Whether the contract is a call or put.
    """

    symbol: str
    underlying_symbol: str
    strike: float = Field(gt=0)
    expiration: datetime
    option_type: OptionType


class OptionQuote(BaseModel):
    """Represent a market quote for an option.

    Attributes:
        contract_symbol: Identifier of the quoted contract.
        bid: Highest quoted buying price.
        ask: Lowest quoted selling price.
        timestamp: Quote observation timestamp in UTC.
    """

    contract_symbol: str
    bid: float = Field(ge=0)
    ask: float = Field(ge=0)
    timestamp: datetime


class PricingInputs(BaseModel):
    """Inputs required to calculate a theoretical option price.

    Attributes:
        spot: Current underlying price in currency units.
        strike: Option strike price in currency units.
        time_to_expiry: Remaining time until expiration in years.
        risk_free_rate: Continuously compounded annual rate as a decimal.
        volatility: Annualized volatility as a decimal.
        option_type: Whether to price a call or put.
    """

    spot: float = Field(gt=0)
    strike: float = Field(gt=0)
    time_to_expiry: float = Field(ge=0)
    risk_free_rate: float
    volatility: float = Field(ge=0)
    option_type: OptionType


class OptionGreeks(BaseModel):
    """Represent Black-Scholes option price sensitivities.

    Attributes:
        delta: Price sensitivity to a one-unit change in spot.
        gamma: Change in delta per one-unit change in spot.
        vega: Price sensitivity to a 1.0 change in decimal volatility.
        theta: Price sensitivity to one year of elapsed time.
    """

    delta: float
    gamma: float
    vega: float
    theta: float


class OptionAnalyticsSnapshot(BaseModel):
    """Combined pricing and risk analytics for an option.

    Attributes:
        contract: Option contract being analyzed.
        timestamp: Analytics observation timestamp in UTC.
        market_price: Observed option price per underlying unit.
        theoretical_price: Model-calculated option price.
        implied_volatility: Volatility implied by the market price.
        greeks: Calculated option price sensitivities.
        moneyness: Option's relationship to its strike.
    """

    contract: OptionContract
    timestamp: datetime
    market_price: float = Field(ge=0)
    theoretical_price: float = Field(ge=0)
    implied_volatility: float = Field(ge=0)
    greeks: OptionGreeks
    moneyness: Moneyness
