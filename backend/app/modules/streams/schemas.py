
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel

MAX_TOPIC_LENGTH = 200


class ClientMessage(BaseModel):
    """A control message a browser sends to change what it receives."""

    # TODO: validate the topic with Field(min_length=1, max_length=MAX_TOPIC_LENGTH,
 


class AckMessage(BaseModel):
    """Confirms a subscribe/unsubscribe was applied."""
        # TODO

 


class DataMessage(BaseModel):
    """One piece of data published to a topic."""
    # TODO

class ErrorMessage(BaseModel):
    """Sent when a client message can't be handled. The socket stays open."""
    # TODO