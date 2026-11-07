# protocol.py

`atlasd/protocol.py` defines every message that the daemon and a strategy process can send each other.
It also defines the rules for turning those messages into bytes on the pipe.

Each kind of message is a class:

```python
class Bar(Msg):
    symbol: str
    close: Decimal
    ...
```

Every message inherits from `Msg`. `Msg` gives each message a tag: a field named `t` that
holds the message's type name. When a `Bar` is encoded, the bytes include `"t": "Bar"`.
The consumer (strategy process) reads the tag first, so it knows which kind of message
arrived and which event it should build.

A `Bar` is sent through a pipe as:

```json
{"t": "Bar", "symbol": "AAPL", "timeframe": "1m", "close": "187.25", ...}
```

## Message Types

There are two types of messages to be sent through the pipe from _router <---> strategy process_

```python
RouterMsg = Start | Bar | OrderUpdate      # daemon -> strategy
StrategyMsg = Ready | Submit               # strategy -> daemon
```

The strategy process runs outside the daemon and it submits orders back to the router.
The router will then send the order to the risk gate then the order manager and so on.
The important consideration is that strategies only talk to the **Event Router**.

## Message Framing

A pipe is a continuous stream of bytes, so we need to mark where messages end and begin.
`protocol.py` defines this set of rules.

Every message is sent as a **Frame**.
Frames are a 4 byte big-endian length followed by a msgpack body.

```text
[length: 88][88 bytes of message][length: 32][32 bytes of message]...
```

`encode()` builds a **frame**. It turns the message into bytes and puts the length in front.

`read_frame()` reads one **frame**. It reads the 4 byte length first, then reads exactly that
many bytes and decodes them into a message.

_A frame larger than 16 MB is rejected._

This protects the daemon from a broken or misbehaving strategy that sends a garbage length.
