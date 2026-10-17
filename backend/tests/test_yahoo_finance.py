import pytest

from packages.yahoo_finance.yahoo_stream import stream_prices


def ignore_message(message):
    pass


def test_empty_symbols():
    with pytest.raises(ValueError):
        stream_prices([], ignore_message)


def test_invalid_messenger():
    with pytest.raises(TypeError):
        stream_prices(["BTC-USD"], "bye") # pyright: ignore[reportArgumentType]
