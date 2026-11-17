"""WebSocket endpoint that lets browsers subscribe to live data topics."""

from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket

from app.modules.streams.dependencies import get_stream_router
from app.modules.streams.hub import Connection, StreamRouter

router = APIRouter()


@router.websocket("/ws")
async def stream_socket(
    websocket: WebSocket,
    hub: Annotated[StreamRouter, Depends(get_stream_router)],
):
    """
    One socket per browser tab. The client sends subscribe/unsubscribe messages
    (see schemas.py) and the server pushes data only for the topics it's subscribed to.

    Implementation:
        1. await websocket.accept()
        2. conn = hub.connect()
        3. Start _send_loop(websocket, conn) as a background asyncio task
        4. Loop forever: raw = await websocket.receive_text(); _handle_client_message(...)
        5. Stop on WebSocketDisconnect
        6. In a `finally`: cancel + await the sender task, then hub.disconnect(conn)
           (cleanup must run however the socket ends, or the hub leaks subscriptions)
    """
    # TODO: implement
    raise NotImplementedError


async def _send_loop(websocket: WebSocket, conn: Connection) -> None:
    """
    Drain the connection's queue to the socket until it closes.

    Implementation:
        Loop: message = await conn.next_message(); await websocket.send_json(message).
        If the socket is already closed (WebSocketDisconnect / RuntimeError), just return;
        the receive loop in stream_socket() does the cleanup.
    """
    # TODO: implement
    raise NotImplementedError


def _handle_client_message(hub: StreamRouter, conn: Connection, raw: str) -> None:
    """
    Apply one client message. Bad input gets an error reply, never a crash.

    Implementation:
        - Parse `raw` with json.loads, then ClientMessage.model_validate(...)
        - Invalid JSON or ValidationError -> conn.push_control(ErrorMessage(...).model_dump())
        - op == "subscribe"   -> hub.subscribe(); reply AckMessage(op="subscribed")
                                 (TooManyTopicsError -> ErrorMessage with the topic)
        - op == "unsubscribe" -> hub.unsubscribe(); reply AckMessage(op="unsubscribed")
        Replies go through conn.push_control (not websocket.send_*) so only the sender
        task ever writes to the socket.
    """
    # TODO: implement
    raise NotImplementedError
