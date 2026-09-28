# To validate that class atributes from schemas.py are valid inputs

def ValidateOptionContract(OptionContract: contract) -> bool:

    if (contract.strike <= 0):
        raise ValueError("Error: Invalid price")

    if (not math.isfinite(contract.strike)):
        raise ValueError("Error: non-finite input")

    return True

def ValidateOptionQuote(OptionQuote: quote) -> bool:

    if (quote.bid < 0):
        raise ValueError("Error: Invalid bid")

    if (quote.ask < 0):
        raise ValueError("Error: Invalid ask")

    if (
    (not math.isfinite(quote.bid)) or
    (not math.isfinite(quote.ask))):
        raise ValueError("Error: non-finite input")

    return True

def ValidateOptionPricing(priceInput: PricingInputs) -> bool:

    if (
    priceInput.spot <= 0 or 
    priceInput.strike <= 0):
        raise ValueError("Error: Invalid price value")

    if (priceInput.time_to_expiry < 0):
        raise ValueError("Error: Invalid time to expiration")

    if (priceInput.volatility < 0):
        raise ValueError("Error: Invalid volatility")

    if (
    (not math.isfinite(priceInput.spot)) or 
    (not math.isfinite(priceInput.strike)) or
    (not math.isfinite(priceInput.time_to_expiry)) or
    (not math.isfinite(priceInput.volatility)) or
    (not math.isfinite(priceInput.risk_free_rate))):
        raise ValueError("Error: non-finite input")

    return True

def ValidateOptionGreeks(OptionGreeks: greeks) -> bool:

    if (
    (not math.isfinite(greeks.delta)) or
    (not math.isfinite(greeks.gamma)) or
    (not math.isfinite(greeks.vega)) or
    (not math.isfinite(greeks.theta))):
        raise ValueError("Error: non-finite input")

    return True

# long af function name :sob:
def ValidateOptionAnalyticsSnapshot(OptionAnalyticsSnapshot: analyticSnapshot) -> bool:

    if (analyticSnapshot.market_price < 0):
        raise ValueError("Error: Invalid market price")

    if (analyticSnapshot.theoretical_price < 0):
        raise ValueError("Error: Invalid theoretical price")

    if (analyticSnapshot.implied_volatility < 0):
        raise ValueError("Error: Invalid implied volatility")

    if (
    (not math.isfinite(analyticSnapshot.market_price)) or
    (not math.isfinite(analyticSnapshot.market_price)) or 
    (not math.isfinite(analyticSnapshot.market_price))):
        raise ValueError("Error: non-finite input")

    return True