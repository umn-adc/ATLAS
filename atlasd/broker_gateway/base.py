from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import ClassVar

import msgspec

from atlas_brokers.base import BrokerOrders
from atlas_brokers.models import Fill, Instrument
from atlasdaemon.broker_gateway.models import Account, BrokerAck, Position, RateLimit, Reconnected


class BrokerClient[O: msgspec.Struct, U: msgspec.Struct](ABC):
    """
    Talks to one broker account. Holds its API keys, so it runs in the daemon only.

    Request methods raise only BrokerRejected, BrokerUnavailable or RateLimited.
    """

    orders: BrokerOrders[O, U]  # which broker's orders this client sends
    account_id: str
    rate_limit: ClassVar[RateLimit]  # enforced by the gateway, one limiter per account

    # Connection
    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    # Everything this account can trade, with current tick size, lot size, etc.
    @abstractmethod
    async def instruments(self) -> list[Instrument]: ...

    # Orders. cid is the client order id; the daemon never reuses one.
    @abstractmethod
    async def submit(self, cid: str, order: O) -> BrokerAck: ...

    @abstractmethod
    async def replace(self, cid: str, new_cid: str, order: O) -> BrokerAck: ...

    @abstractmethod
    async def cancel(self, cid: str) -> None: ...

    # Lookups, used after a timeout or reconnect. get_order returns None if the broker never saw it.
    @abstractmethod
    async def get_order(self, cid: str) -> U | None: ...

    @abstractmethod
    async def open_orders(self) -> list[U]: ...

    # Account. positions() is account-wide and only cross-checks the Order Manager.
    @abstractmethod
    async def positions(self) -> list[Position]: ...

    @abstractmethod
    async def account(self) -> Account: ...

    # Stream of order updates and fills. Yields Reconnected after any gap.
    @abstractmethod
    def events(self) -> AsyncIterator[U | Fill | Reconnected]: ...
