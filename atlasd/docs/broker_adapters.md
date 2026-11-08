# Broker adapters

A **broker adapter** is everything ATLAS needs to trade on one broker. 

Each adapter is split into two halves:

- The **orders** half says what an order for this broker looks like. Used by *Strategy Processes* and the *Atlas Daemon*
- The **client** actually talks to the broker over the network. Used by the *Atlas Daemon* only

The two halves live in different packages:

```text
atlas_brokers/
└── <broker_name>/
    └── orders.py

atlasdaemon/broker_gateway/
└── <broker_name>/
    └── client.py
```

These files are separated so API keys are kept outside of strategy processes.
A strategy can build and check an order but it can never send one on its own.
Every order goes through the *Atlas Daemon* and the Risk Gate.

IMPORTANT: There is no shared `Order` type for users to write.
`BrokerOrders` can have default orders, but a user must specify which broker they are
sending orders too. This is because brokers ask for very different order and data shapes.

It would be nice to have an interface or methods that allows users to write
strategies that easily swap between which brokers they send orders at strategy runtime.

## Broker Orders

`orders.py` defines the broker's order as a tagged msgspec Struct. The tag is the broker's name:

```python
class AlpacaOrder(msgspec.Struct, tag="alpaca"):
    instrument_id: str
    side: Literal["buy", "sell"]
    type: Literal["market", "limit", "stop", "stop_limit", "trailing_stop"]
    time_in_force: Literal["day", "gtc", "opg", "cls", "ioc", "fok"]
    qty: Decimal | None = None
    notional: Decimal | None = None
    limit_price: Decimal | None = None
    stop_price: Decimal | None = None
    order_class: Literal["simple", "bracket", "oco", "oto"] = "simple"
```

`orders.py` also defines four functions:

`validate(order, inst, now)` checks the broker's own rules, like lot size, tick size, minimum
notional and trading hours. It returns a reason string, or `None` if the order is fine.

`risk_view(order, inst, ref_px)` turns the order into a `RiskView`. The Risk Gate only reads
`RiskView`, so it does not need to know anything about any one broker. `ref_px` is a price to use
when the order has none, like the last trade for a market order:

```python
class RiskView(msgspec.Struct):
    instrument_id: str
    side: Side
    qty_estimate: Decimal
    notional_estimate: Decimal
    reduces_position: bool
```

`normalize(update)` turns the broker's order update into the common `OrderState`.

`to_sim(order)` turns the order into a `SimOrder` for paper trading, or `None` if paper cannot
simulate it.

## Order helpers

Users should not have to fill in a full order struct. `orders.py` gives them short helpers that
build one:

```python
from atlas import Strategy, on, Bars
from atlas.brokers import alpaca


class SmaCross(Strategy):
    BROKER = alpaca

    @on(Bars("AAPL", "1m"))
    async def bar(self, ctx, bar):
        await ctx.submit(alpaca.market("AAPL", "buy", qty=10))
```

`BROKER` is the broker's `BrokerOrders` object, so a typo fails on import.

A bare symbol like `"AAPL"` means that symbol on this broker's venue, `"AAPL.ALPACA"`.

## Instruments

An **instrument** is one tradable thing on one venue. Every instrument has a canonical id,
`<SYMBOL>.<VENUE>`:

```text
AAPL.ALPACA         BTC-USD.BINANCEUS
```

Brokers spell the same asset differently (`BTCUSD`, `BTC/USD`, `BTC-USD`). The canonical id is
what ATLAS uses everywhere: subscriptions, orders, positions and the Risk Gate. The broker's own
spelling lives in `Instrument.symbol`, and only the client uses it.

```python
class Instrument(msgspec.Struct):
    id: str                       # "AAPL.ALPACA"
    venue: str
    symbol: str                   # the broker's own spelling
    tick_size: Decimal
    lot_size: Decimal
    min_qty: Decimal
    min_notional: Decimal | None
    tradable: bool
    shortable: bool
```

Trading rules change, so instruments are not hardcoded. The client loads them from the broker
when the daemon starts. The daemon sends each deployment its instruments in `Start`, so
`validate()` in the strategy process checks against real rules.

## Broker Adapter Base Classes

Every adapter inherits from two base classes. Anything marked `@abstractmethod` is **required**.
Python refuses to create an adapter that is missing one.

```python
class BrokerOrders[O, U](ABC):               # atlas_brokers/base.py
    name: str                                # must equal the order type's tag
    version: int                             # bump on any change to O or U
    order_type: type[O]
    update_type: type[U]
    def validate(self, order, inst, now) -> str | None
    def risk_view(self, order, inst, ref_px) -> RiskView
    def normalize(self, update) -> OrderState
    def to_sim(self, order) -> SimOrder | None

class BrokerClient[O, U](ABC):               # atlasdaemon/broker_gateway/base.py
    orders: BrokerOrders[O, U]
    rate_limit: RateLimit
    account_id: str
    async def connect(self) -> None
    async def close(self) -> None
    async def instruments(self) -> list[Instrument]
    async def submit(self, cid, order) -> BrokerAck
    async def replace(self, cid, new_cid, order) -> BrokerAck
    async def cancel(self, cid) -> None
    async def get_order(self, cid) -> U | None
    async def open_orders(self) -> list[U]
    async def positions(self) -> list[Position]
    async def account(self) -> Account
    def events(self) -> AsyncIterator[U | Fill | Reconnected]
```

Order helpers are **optional**. An adapter only adds the ones its venue supports. Polymarket only
takes limit orders, so its adapter has `limit()` and no `market()`.

If an adapter does add a helper with a standard name, it must use the standard signature:

```python
class SupportsMarket(Protocol):
    def market(self, instrument_id: str, side: Side, qty: Decimal) -> Order

class SupportsLimit(Protocol):
    def limit(self, instrument_id: str, side: Side, qty: Decimal, price: Decimal) -> Order
```

This keeps names the same everywhere they exist. A strategy that only uses helpers both brokers
have can move between them by changing one import. Helpers that only one broker has, like
`alpaca.bracket()`, have no standard signature.

_A helper must never silently turn into an order with different risk._ If an adapter emulates a
market order with an aggressive limit order, its docs must say so.

`ctx.submit` runs `validate()` inside the strategy process before anything is sent. A bad order
raises an error on the user's own line, in backtests too. The daemon still checks it again.

A missing helper is caught by the type checker, or by the paper run every deployment must pass
before it can go live.

## The client

`client.py` is the half that talks to the broker. It inherits from `BrokerClient` and holds
the API keys for **one account**. Paper and live keys are different accounts, so they are
different client instances.

## Adding a broker

1. `atlas_brokers/<name>/orders.py`: a `BrokerOrders` subclass with its tagged order type,
   update type, `validate()`, `risk_view()`, `normalize()`, `to_sim()`, and whichever helpers
   the venue supports
2. `atlasdaemon/broker_gateway/<name>/client.py`: a `BrokerClient` subclass
