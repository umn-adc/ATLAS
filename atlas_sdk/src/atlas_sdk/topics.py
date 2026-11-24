from typing import Literal

import msgspec

Timeframe = Literal["1m", "5m", "15m", "1h", "1d"]


def _topic_tag(class_name: str) -> str:
    return class_name.removesuffix("Topic").lower()  # BarTopic -> "bar"


class Topic(msgspec.Struct, frozen=True, kw_only=True, tag=_topic_tag, tag_field="topic"):
    """Base class for Topics: a stream of data a deployment subscribes to"""

    source: str  # who delivers the data, e.g. "alpaca-iex"


# frozen=True is repeated on each subclass for pyright; msgspec already inherits it.


class BarTopic(Topic, frozen=True):
    instrument_id: str
    timeframe: Timeframe


class QuoteTopic(Topic, frozen=True):
    instrument_id: str


class TradeTopic(Topic, frozen=True):
    instrument_id: str


class NewsTopic(Topic, frozen=True):
    symbol: str  # news is about a company, not a venue


# msgspec can't decode into the base class, so fields sent through the pipe use this union.
AnyTopic = BarTopic | QuoteTopic | TradeTopic | NewsTopic
