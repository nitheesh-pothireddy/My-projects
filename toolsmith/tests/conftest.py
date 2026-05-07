"""Shared pytest fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def gold_current_weather() -> dict:
    return {
        "tool": "get_current_weather",
        "arguments": {"latitude": 17.385, "longitude": 78.487, "temperature_unit": "celsius"},
    }


@pytest.fixture
def gold_refusal() -> dict:
    return {"tool": None, "reason": "Air quality is not in the available tool catalogue."}
