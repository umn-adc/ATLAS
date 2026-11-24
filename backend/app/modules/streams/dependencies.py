"""Dependency providers for the streams module."""

from fastapi.requests import HTTPConnection

from app.modules.streams.hub import StreamRouter


def get_stream_router(connection: HTTPConnection) -> StreamRouter:
    # HTTPConnection works for both HTTP requests and WebSockets.
    # TODO: create_app() in main.py must set app.state.stream_router = StreamRouter()
    return connection.app.state.stream_router
