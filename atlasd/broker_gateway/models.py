from datetime import datetime
from decimal import Decimal

import msgspec


class BrokerAck(msgspec.Struct, frozen=True):
    cid: str  # client order id, assigned by atlasdaemon
    broker_id: str  # id the broker gave the order
    ts: datetime


class Position(msgspec.Struct, frozen=True):
    instrument_id: str
    qty: Decimal  # negative when short
    avg_px: Decimal


class Account(msgspec.Struct, frozen=True):
    cash: Decimal
    equity: Decimal
    buying_power: Decimal


class RateLimit(msgspec.Struct, frozen=True):
    requests: int
    per_seconds: float


class Reconnected(msgspec.Struct, frozen=True):
    """The event stream dropped and came back. Events may have been missed."""


class BrokerRejected(Exception):
    """The broker refused it. The order goes to REJECTED."""


class BrokerUnavailable(Exception):
    """No answer, e.g. a timeout. The order goes to UNKNOWN and is reconciled."""


class RateLimited(Exception):
    """Too many requests. Retry after `retry_after` seconds."""

    def __init__(self, retry_after: float):
        super().__init__(f"rate limited, retry after {retry_after}s")
        self.retry_after = retry_after
