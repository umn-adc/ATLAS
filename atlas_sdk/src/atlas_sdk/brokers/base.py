from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Protocol, runtime_checkable

import msgspec

from atlas_sdk.brokers.models import Instrument, OrderState, RiskView, Side, SimOrder


class BrokerOrders[O: msgspec.Struct, U: msgspec.Struct](ABC):
    """Builds and checks one broker's orders. No network, no keys: strategies import this too."""

    name: str  # must equal order_type's tag, e.g. "alpaca"
    version: int  # bump when order_type or update_type changes
    order_type: type[O]
    update_type: type[U]

    # Is this order legal on this broker? Returns a reason, or None if it is.
    @abstractmethod
    def validate(self, order: O, inst: Instrument, now: datetime) -> str | None: ...

    # Numbers the Risk Gate checks. ref_price prices orders that have no price, like market orders.
    @abstractmethod
    def risk_view(self, order: O, inst: Instrument, ref_price: Decimal) -> RiskView: ...

    # The broker's order update -> common OrderState.
    @abstractmethod
    def normalize(self, update: U) -> OrderState: ...

    # Order -> something paper trading can fill, or None if it can't fill it faithfully.
    @abstractmethod
    def to_sim(self, order: O) -> SimOrder | None: ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        order_type = cls.__dict__.get("order_type")
        if order_type is not None and order_type.__struct_config__.tag != cls.name:
            raise TypeError(f"{cls.__name__}.order_type must be tagged {cls.name!r}")


# Optional helpers. A broker adds them only if its venue supports them,
# and must use exactly these signatures when it does.


@runtime_checkable
class SupportsMarket(Protocol):
    def market(self, instrument_id: str, side: Side, qty: Decimal) -> msgspec.Struct: ...


@runtime_checkable
class SupportsLimit(Protocol):
    def limit(
        self, instrument_id: str, side: Side, qty: Decimal, price: Decimal
    ) -> msgspec.Struct: ...
