"""Validate strategy parameters against what a version declares it expects."""

from dataclasses import dataclass
from typing import Any, Literal

ParameterType = Literal["int", "float", "str", "bool"]


@dataclass(frozen=True)
class ParameterSpec:
    """One parameter a strategy version expects."""

    name: str
    type: ParameterType
    required: bool = True


def validate_parameters(specs: list[ParameterSpec], supplied: dict[str, Any]) -> list[str]:
    """
    Check supplied parameters against a version's declared specs.

    Args:
        specs: Parameters the version expects
        supplied: Parameters provided for the deployment

    Returns:
        list[str]: Human-readable errors. Empty means valid.

    Implementation:
        Report missing required parameters, unknown parameters,
        and values whose type doesn't match the spec.
    """
    raise NotImplementedError
