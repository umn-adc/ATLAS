import asyncio
import struct
from datetime import datetime
from decimal import Decimal

import msgspec

from atlas_brokers.models import Fill, Instrument, OrderState

PROTOCOL_VERSION = 1
MAX_FRAME = 16 * 1024 * 1024  # 16 MB
_HEADER = struct.Struct(">I")  # big-endian unsigned 4-byte int


class Msg(msgspec.Struct, tag=True, tag_field="t"):
    """Base for all wire messages. Tag is the class name."""


# atlasdaemon -> strategy


class Start(Msg):
    version: int  # protocol version
    brokers: dict[str, int]  # broker name -> BrokerOrders.version, must match Ready.brokers
    instruments: list[Instrument]  # everything this deployment may trade
    params: dict
    state: dict  # last State, empty on first run


class Bar(Msg):
    instrument_id: str  # "<SYMBOL>.<VENUE>", so the venue is always known
    source: str  # who delivered it, e.g. "alpaca-iex", "alpaca-sip"
    timeframe: str
    ts_event: datetime  # bar start, stamped by the venue
    ts_recv: datetime  # when atlasdaemon received it
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal


class SubmitAck(Msg):
    req_id: int
    cid: str  # client order id, assigned by atlasdaemon
    created_at: datetime


class Error(Msg):
    req_id: int
    reason: str


class OrderUpdate(Msg):
    cid: str
    state: OrderState  # common fields
    raw: msgspec.Raw  # the broker's own update


class Filled(Msg):
    fill: Fill


class Stop(Msg):
    """Shut down gracefully. Strategy should send State, then exit."""


# strategy -> atlasdaemon


class Ready(Msg):
    version: int
    brokers: dict[str, int]  # broker name -> BrokerOrders.version the runner was built with


class Submit(Msg):
    req_id: int
    order: msgspec.Raw  # a tagged broker order; the tag picks the broker


class Replace(Msg):
    req_id: int
    cid: str  # open order to change
    order: msgspec.Raw  # replacement, same broker


class Cancel(Msg):
    req_id: int
    cid: str


class State(Msg):
    state: dict  # handed back in Start.state on restart


RouterMsg = Start | Bar | SubmitAck | Error | OrderUpdate | Filled | Stop
StrategyMsg = Ready | Submit | Replace | Cancel | State

_encoder = msgspec.msgpack.Encoder()
router_decoder = msgspec.msgpack.Decoder(RouterMsg)  # used by strategies
strategy_decoder = msgspec.msgpack.Decoder(StrategyMsg)  # used by atlasdaemon


def encode(msg: Msg) -> bytes:
    """
    Encode a message as a length-prefixed frame.

    Args:
        msg: Message to encode

    Returns:
        Frame bytes
    """
    body = _encoder.encode(msg)
    if len(body) > MAX_FRAME:
        raise ValueError(f"frame too large: {len(body)}")
    return _HEADER.pack(len(body)) + body


async def write_frame(writer: asyncio.StreamWriter, msg: Msg) -> None:
    """
    Encode a message and write it to a stream, waiting for the buffer to drain.

    Args:
        writer: Stream to write to
        msg: Message to send
    """
    writer.write(encode(msg))
    await writer.drain()


async def read_frame(reader: asyncio.StreamReader, decoder: msgspec.msgpack.Decoder) -> Msg:
    """
    Read one frame from a stream and decode it.

    Args:
        reader: Stream to read from
        decoder: Decoder for the expected message union

    Returns:
        Decoded message

    Raises:
        asyncio.IncompleteReadError: Stream closed mid-frame
        ValueError: Frame exceeds MAX_FRAME
        msgspec.ValidationError: Body is not a valid message for this decoder
    """
    (n,) = _HEADER.unpack(await reader.readexactly(_HEADER.size))
    if n > MAX_FRAME:
        raise ValueError(f"frame too large: {n}")
    return decoder.decode(await reader.readexactly(n))
