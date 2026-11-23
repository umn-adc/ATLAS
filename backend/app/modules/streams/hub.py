"""
StreamRouter: fans out continuous data to only the sockets that asked for it.

Producers call `publish(topic, payload)`. The router looks up who is subscribed
to that topic and queues the message on each of those connections. A separate
sender task per socket drains its queue (see router.py), so a slow browser never
blocks a producer or any other browser.

This file has no FastAPI imports on purpose so it can be unit tested directly.
Same ideas as the daemon's message bus (atlasdaemon/docs/message_bus.md):
- topic -> subscribers map
- bounded per-connection queue; when full, the oldest *data* is dropped
- control messages (acks/errors) are never dropped and go out before data
- every topic has its own `seq` counter so clients can detect gaps
"""

import asyncio
from collections import defaultdict, deque
from typing import Any

DEFAULT_MAX_QUEUE = 256
DEFAULT_MAX_TOPICS_PER_CONNECTION = 64


class TooManyTopicsError(Exception):
    """A connection tried to subscribe to more topics than allowed."""


class Connection:
    """
    One subscriber (usually one browser tab).

    Holds the topics it's subscribed to and the messages waiting to be sent.
    """

    def __init__(self, max_queue: int = DEFAULT_MAX_QUEUE) -> None:
        self.topics: set[str] = set()
        self.dropped = 0  # data messages discarded because the queue was full
        self._control: deque[dict[str, Any]] = deque()
        # deque(maxlen=...) discards from the left (oldest) when appending to a full deque
        self._data: deque[dict[str, Any]] = deque(maxlen=max_queue)
        # Set whenever something is queued so next_message() can wake up
        self._ready = asyncio.Event()

    def push_control(self, message: dict[str, Any]) -> None:
        """
        Queue a message that must never be dropped (ack, error).

        Implementation:
            Append to self._control and set self._ready.
        """
        #Ignore for now
        raise NotImplementedError

    def push_data(self, message: dict[str, Any]) -> None:
        """
        Queue a data message, dropping the oldest one if the queue is full.

        Implementation:
            If self._data is already at maxlen, increment self.dropped.
            Append to self._data (the deque drops the oldest for you) and set self._ready.
        """
        if (len(self._data) == self._data.maxlen):
            self.dropped += 1
        self._data.append(message)
        self._ready.set()

    def pending(self) -> int:
        """Number of messages waiting to be sent."""
        return (len(self._control) + len(self._data))

    async def next_message(self) -> dict[str, Any]:
        """
        Wait for the next message to send. Control messages go first.

        Implementation:
            Loop: pop from self._control if non-empty, else from self._data if
            non-empty, else clear self._ready and await self._ready.wait().
        """
        while True:
            if (len(self._control) > 0):
                return self._control.popleft()
            elif (len(self._data) > 0):
                return self._data.popleft()
            else:
                self._ready.clear()
                await self._ready.wait()


class StreamRouter:
    """In-process pub/sub hub. One instance per backend app (stored on app.state)."""

    def __init__(
        self,
        max_queue: int = DEFAULT_MAX_QUEUE,
        max_topics_per_connection: int = DEFAULT_MAX_TOPICS_PER_CONNECTION,
    ) -> None:
        self._max_queue = max_queue
        self._max_topics = max_topics_per_connection
        self._subscribers: defaultdict[str, set[Connection]] = defaultdict(set)  # topic -> conns
        self._seq: defaultdict[str, int] = defaultdict(int)  # topic -> last seq published
        self._connections: set[Connection] = set()

    # --- connections ---

    def connect(self) -> Connection:
        """
        Register a new subscriber.

        Returns:
            Connection: A new connection with an empty queue and no topics
        """
        # TODO: implement
        raise NotImplementedError

    def disconnect(self, conn: Connection) -> None:
        """
        Remove a subscriber and all of its subscriptions.

        Must be safe to call more than once for the same connection.
        """
        # TODO: implement (unsubscribe from every topic in conn.topics, then forget conn)
        raise NotImplementedError

    @property
    def connection_count(self) -> int:
        return len(self._connections)

    # --- subscriptions ---

    def subscribe(self, conn: Connection, topic: str) -> None:
        """
        Start delivering `topic` to `conn`. Subscribing twice is a no-op.

        Raises:
            TooManyTopicsError: If the connection is already at self._max_topics
        """
        # TODO: implement (update both conn.topics and self._subscribers)
        raise NotImplementedError

    def unsubscribe(self, conn: Connection, topic: str) -> None:
        """
        Stop delivering `topic` to `conn`. Unknown topics are ignored.

        Implementation:
            Remove from both conn.topics and self._subscribers[topic].
            Delete the topic key when its last subscriber leaves so the map doesn't grow forever.
        """
        # TODO: implement
        raise NotImplementedError

    def subscriber_count(self, topic: str) -> int:
        """How many connections are subscribed to `topic`."""
        # TODO: implement (careful: don't create an empty entry in the defaultdict)
        raise NotImplementedError

    # --- publishing ---

    def publish(self, topic: str, payload: dict[str, Any]) -> int:
        """
        Send `payload` to every connection subscribed to `topic`.

        Never blocks: messages are queued, not sent.

        Returns:
            int: How many connections the message was queued for

        Implementation:
            Increment self._seq[topic].
            Build a DataMessage (schemas.py) with topic, seq, ts=datetime.now(UTC), payload,
            and turn it into a dict with .model_dump(mode="json"). Build it once, not per conn.
            push_data() it onto each subscriber's Connection.
        """
        # TODO: implement
        # TODO (later): cache the last message per topic and send it on subscribe (snapshot)
        raise NotImplementedError
