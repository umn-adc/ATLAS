from datetime import datetime
from decimal import Decimal
from typing import Literal

import msgspec

Side = Literal["buy", "sell"]
OrderStatus = Literal[
    "new", "accepted", "rejected", "partially_filled", "filled", "canceled", "unknown"
]


class Instrument(msgspec.Struct, frozen=True):
    """One tradable thing on one venue. Loaded from the broker at startup."""

    id: str  # "<SYMBOL>.<VENUE>", e.g. "AAPL.ALPACA", "BTC-USD.BINANCEUS"
    venue: str
    symbol: str  # the broker's own spelling, e.g. "BTCUSD"
    tick_size: Decimal
    qty_step: Decimal
    min_qty: Decimal
    min_notional: Decimal | None
    tradable: bool
    shortable: bool


class RiskView(msgspec.Struct, frozen=True):
    """What the Risk Gate reads for any broker's order."""

    instrument_id: str
    side: Side
    qty_estimate: Decimal
    notional_estimate: Decimal
    reduces_position: bool


class OrderState(msgspec.Struct, frozen=True):
    """Common fields every broker's order update is turned into."""

    status: OrderStatus
    filled_qty: Decimal  # cumulative
    avg_price: Decimal | None
    ts: datetime


class Fill(msgspec.Struct, frozen=True):
    """One execution. Reconnects can replay fills, so they are deduplicated by trade_id."""

    cid: str
    trade_id: str
    qty: Decimal
    price: Decimal
    fee: Decimal
    fee_currency: str
    ts: datetime


class SimOrder(msgspec.Struct, frozen=True):
    """The small set of orders paper trading can fill."""

    instrument_id: str
    side: Side
    qty: Decimal
    type: Literal["market", "limit", "stop", "stop_limit"]
    limit_price: Decimal | None = None
    stop_price: Decimal | None = None
    tif: Literal["day", "gtc", "ioc", "fok"] = "gtc"
    children: tuple["SimOrder", ...] = ()  # exits attached to this order, e.g. a bracket
    oco: bool = False  # filling one child cancels the others
