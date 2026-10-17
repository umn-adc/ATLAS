# Yahoo Finance streamer

Streams Yahoo Finance price updates to a function you provide.

## Setup

Run these commands from ATLAS's `backend` folder:

```bash
uv sync
```

## Run the example

From `backend`, run:

```bash
uv run python -m packages.yahoo_finance.yahoo_stream
```

The example subscribes to AAPL and BTC-USD and prints updates.
Press Control+C to stop.

## Use from another file

Run your calling script from `backend` using `uv run python`.

```python
from packages.yahoo_finance.yahoo_stream import stream_prices


def receive_update(message):
    print(message)


stream_prices(["AAPL", "BTC-USD"], receive_update)
```

`symbols` must be a non-empty list of ticker symbols.
The callback must accept one update dictionary.

## Run validation tests

From `backend`, run:

```bash
uv run pytest tests/test_yahoo_finance.py -v
```

## Limitations

Updates are dictionaries, and fields can differ between symbols.
Updates do not arrive at a guaranteed fixed interval.

The stream runs until interrupted or the connection ends.
It does not automatically reconnect when streaming ends.