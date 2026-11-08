import asyncio
from datetime import UTC, datetime
from decimal import Decimal

import msgspec
import pytest

from atlas_brokers.models import Fill, Instrument, OrderState
from atlasdaemon.protocol import (
    _HEADER,
    MAX_FRAME,
    Bar,
    Filled,
    OrderUpdate,
    Ready,
    Start,
    Stop,
    Submit,
    encode,
    read_frame,
    router_decoder,
    strategy_decoder,
)

TS = datetime(2026, 1, 2, 14, 30, tzinfo=UTC)
PX = Decimal("187.25")
RAW = msgspec.Raw(msgspec.msgpack.encode({"type": "alpaca", "symbol": "AAPL"}))
AAPL = Instrument(
    "AAPL.ALPACA", "ALPACA", "AAPL", Decimal("0.01"), Decimal(1), Decimal(1), None, True, True
)


def reader_with(data: bytes) -> asyncio.StreamReader:
    reader = asyncio.StreamReader()
    reader.feed_data(data)
    reader.feed_eof()
    return reader


@pytest.mark.parametrize(
    "msg, decoder",
    [
        (Start(1, {"alpaca": 1}, [AAPL], {}, {}), router_decoder),
        (
            Bar("AAPL.ALPACA", "alpaca-iex", "1m", TS, TS, PX, PX, PX, PX, Decimal(1)),
            router_decoder,
        ),
        (OrderUpdate("c1", OrderState("filled", Decimal(5), PX, TS), RAW), router_decoder),
        (Filled(Fill("c1", "t1", Decimal(5), PX, Decimal("0.01"), "USD", TS)), router_decoder),
        (Stop(), router_decoder),
        (Submit(1, RAW), strategy_decoder),
    ],
)
async def test_round_trip(msg, decoder):
    reader = reader_with(encode(msg) + encode(msg))
    assert await read_frame(reader, decoder) == msg
    assert await read_frame(reader, decoder) == msg


async def test_oversize_frame_rejected():
    with pytest.raises(ValueError):
        await read_frame(reader_with(_HEADER.pack(MAX_FRAME + 1)), strategy_decoder)


async def test_truncated_frame():
    with pytest.raises(asyncio.IncompleteReadError):
        await read_frame(reader_with(encode(Ready(1, {}))[:-1]), strategy_decoder)


async def test_wrong_direction_rejected():
    with pytest.raises(msgspec.ValidationError):
        await read_frame(reader_with(encode(Stop())), strategy_decoder)
