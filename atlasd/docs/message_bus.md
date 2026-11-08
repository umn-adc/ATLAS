# message_bus.py

The *Message Bus* in the *Atlas Daemon* broadcasts and moves messages between
the strategy processes and everything else inside the daemon.

It's the only code that reads and writes the strategy pipes.
It decodes what a strategy sends (`Submit`, `Cancel`, ...) and passes it elsewhere.
It takes data from the *Market Data Feed Handler* and order events from brokers and 
delivers it to only the strategies that should get it.

Each strategy delineates exactly what messages it wants to recieve through *Subscriptions*

## Subscriptions

Strategies subscribe to subscriptions by *topic*. A topic is a data type plus the *instrument*,
source, and timeframe for the data. For example: `bar:AAPL.ALPACA:alpaca:1m` or `news:AAPL`.

A strategy lists its topics in *Ready*, and the bus keeps a map from each topic to the 
strategy processes that want it. When market data arrives, the bus looks up its topic and sends
it only to those deployments.

**Currently, we send everything and let strategies filter. This is simple but strategies 
do extra decoding work. **

Order events skip topics. Instead, the bus looks up the `cid`, finds the strategy process that owns it,
and delivers to that one strategy only.

## Message Queue

Each strategy deployment gets its own outbound queue with a fixed maximum size.
When the queue fills, the rule depends on what's in it.

Order events are never dropped, but the oldest (stale) data is dropped.
The bus counts the drops and tells the strategy how much it missed.

This architecture could use obvious improvements
