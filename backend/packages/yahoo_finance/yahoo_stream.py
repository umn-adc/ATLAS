from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import yfinance as yf


def show_update(message):
    symbol = message["id"]
    currency = message.get("currency", "")
    price = message["price"]
    timestamp = int(message["time"])
    update_time = datetime.fromtimestamp(
        timestamp / 1000,
        tz=UTC,
    )

    print(f"{symbol}: {price} {currency}, time: {update_time}")


def stream_prices(symbols: list[str], messenger: Callable[[dict[str, Any]], None]) -> None:
    """Stream Yahoo Finances updates to callback

    symbols = list of ticker symbols
    messenger = a caller that accepts one dictionary input

    Runs until Ctrl+C is typed

    """
    if not symbols:
        raise ValueError("Provide at least one symbol.")
    if not callable(messenger):
        raise TypeError("messenger should be callable, such as a function.")
    try:
        with yf.WebSocket() as ls:
            ls.subscribe(symbols)
            ls.listen(messenger)
    except KeyboardInterrupt:
        pass

    print("\nStream closed.")


def main():
    stream_prices(["AAPL", "BTC-USD"], show_update)


if __name__ == "__main__":
    main()
