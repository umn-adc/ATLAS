import asyncio
import struct
from datetime import datetime
from decimal import Decimal

import msgspec

PROTOCOL_VERSION = 1
MAX_FRAME = 16 * 1024 * 1024  # 16 MB
_HEADER = struct.Struct(">I")  # big-endian unsigned 4-byte int


class Msg(msgspec.Struct, tag=True, tag_field="t"):
    """Base for all wire messages. Tag is the class name."""


# atlasd -> strategy


class Start(Msg):
    version: int  # protocol version
    params: dict
    state: dict


class Bar(Msg):
    symbol: str
    timeframe: str
    ts: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal


class OrderUpdate(Msg):
    cid: str  # client order id
    status: str


# strategy -> atlasd


class Ready(Msg):
    version: int


class Submit(Msg):
    req_id: int  # request id
    order: dict


RouterMsg = Start | Bar | OrderUpdate
StrategyMsg = Ready | Submit

_encoder = msgspec.msgpack.Encoder()


def encode(msg: Msg) -> bytes:
    """
    Encode a message as a length-prefixed frame.

    Args:
        msg: Message to encode

    Returns:
        Frame bytes
    """
    body = _encoder.encode(msg)
    return _HEADER.pack(len(body)) + body


async def read_frame(
    reader: asyncio.StreamReader, decoder: msgspec.msgpack.Decoder
) -> Msg:
    """
    Read one frame from a stream and decode it.

    Args:
        reader: Stream to read from
        decoder: Decoder for the expected message union

    Returns:
        Decoded message
    """
    (n,) = _HEADER.unpack(await reader.readexactly(_HEADER.size))
    if n > MAX_FRAME:
        raise ValueError(f"frame too large: {n}")
    return decoder.decode(await reader.readexactly(n))
