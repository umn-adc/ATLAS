import logging
import os

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DEFAULT_LOG_LEVEL = "INFO"

_UVICORN_LOGGERS = ("uvicorn", "uvicorn.error", "uvicorn.access")


def setup_logging() -> None:
    """Configure app logging. Level comes from the LOG_LEVEL env var (default INFO)."""
    level_name = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
    level = logging.getLevelName(level_name)
    if not isinstance(level, int):
        level = logging.INFO

    root = logging.getLogger()
    root.setLevel(level)

    # Idempotent: only attach our handler once
    if not any(getattr(h, "_atlas", False) for h in root.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        handler._atlas = True  # type: ignore[attr-defined]
        root.addHandler(handler)

    # Uvicorn installs its own handlers; stop its records from also reaching root
    for name in _UVICORN_LOGGERS:
        uvicorn_logger = logging.getLogger(name)
        if uvicorn_logger.handlers:
            uvicorn_logger.propagate = False
