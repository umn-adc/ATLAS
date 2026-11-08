# message_bus.py

The *Message Bus* in the *Atlas Daemon* routes messages between
the deployments and everything else inside the daemon.

It's the only code that reads and writes the deployment pipes.
It decodes what a deployment sends (`Submit`, `Cancel`, ...) and passes it elsewhere.
It takes data from the *Market Data Feed Handler* and order events from brokers and 
delivers it to only the deployments that should get it.

Each deployment delineates exactly what messages it wants to receive through *Subscriptions*

## Subscriptions

Deployments subscribe by *topic*. A topic is a data type plus the *instrument*,
source, and timeframe for the data. For example: `bar:AAPL.ALPACA:alpaca:1m` or `news:AAPL`.

A deployment lists its topics in *Ready*, and the bus keeps a map from each topic to the 
deployments that want it. When market data arrives, the bus looks up its topic and sends
it only to those deployments.

Order events skip topics. Instead, the bus looks up the `cid`, finds the deployment that owns it,
and delivers to that one deployment only.

## Message Queue

Each deployment gets its own outbound queue with a fixed maximum size.
When the queue fills, the rule depends on what's in it.

Order events are never dropped, but the oldest (stale) data is dropped.
The bus counts the drops and tells the deployment how much it missed.
A deployment's order events are sent before its queued data.

This architecture could use obvious improvements

## Starting a process with the bus

The *Supervisor* starts a deployment's process and hands its pipes to the bus.

To join a bus:
1. The bus sends `Start`
2. It waits for `Ready`, If `Ready` doesn't arrive within a time limit, or carries the wrong version,
the bus reports failure to the Supervisor and the deployment doesn't go live.
3. Once `Ready` arrives, the bus records the deployment's topics and starts delivering.

To leave the bus, if the pipe closes or a frame is bad, the bus removes the deployment's topics,
drops its queues and tells the Supervisor. The Supervisor decides whether to restart it.

## Strategy requests

When a deployment sends `Submit`, `Replace` or `Cancel`, the bus decodes it and passes it to the *Risk Gate*.
The bus doesn't wait for the order to finish. It moves on to the next message.

The answer (`SubmitAck` or `Error`) comes back later, and the bus sends it to that deployment with the same `req_id`.
`State` goes to the *Ledger* and needs no answer.

Each deployment can have at most 32 requests waiting for an answer.
Past that, its next request gets `Error("too many pending requests")`.
This stops one buggy strategy from flooding the Risk Gate or using up the broker's rate limit.
