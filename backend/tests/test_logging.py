import logging

from app.core.logging import setup_logging


def _reset_root():
    root = logging.getLogger()
    for h in [h for h in root.handlers if getattr(h, "_atlas", False)]:
        root.removeHandler(h)


def test_default_level_is_info(monkeypatch):
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    _reset_root()
    setup_logging()
    assert logging.getLogger().level == logging.INFO


def test_log_level_env_var(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "debug")
    _reset_root()
    setup_logging()
    assert logging.getLogger().level == logging.DEBUG


def test_setup_is_idempotent(monkeypatch):
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    _reset_root()
    setup_logging()
    setup_logging()
    atlas = [h for h in logging.getLogger().handlers if getattr(h, "_atlas", False)]
    assert len(atlas) == 1
