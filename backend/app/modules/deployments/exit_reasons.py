"""Translate strategy process exit codes into readable reasons."""

from enum import StrEnum


class ExitReason(StrEnum):
    """Why a strategy process ended."""

    FINISHED = "finished"
    STOPPED = "stopped"
    KILLED = "killed"
    CRASHED = "crashed"


def exit_reason(returncode: int) -> ExitReason:
    """
    Map a process return code to an ExitReason.

    Args:
        returncode: Process return code. Negative values mean the process was
            ended by that signal number (subprocess convention, e.g. -15 = SIGTERM).

    Returns:
        ExitReason: The readable reason

    Implementation:
        0 -> FINISHED.
        Ended by SIGTERM -> STOPPED.
        Ended by SIGKILL -> KILLED.
        Anything else -> CRASHED.
    """
    raise NotImplementedError
