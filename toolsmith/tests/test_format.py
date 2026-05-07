"""Tests for the chat-template formatter (no GPU, no model needed)."""

from __future__ import annotations

import json

from toolsmith.data.format import to_messages


def test_to_messages_has_three_turns() -> None:
    row = {
        "prompt": "weather in Hyderabad?",
        "completion": {"tool": "get_current_weather", "arguments": {"latitude": 17.4, "longitude": 78.5}},
    }
    msgs = to_messages(row)
    assert [m["role"] for m in msgs] == ["system", "user", "assistant"]
    assert msgs[1]["content"] == "weather in Hyderabad?"
    assert json.loads(msgs[2]["content"])["tool"] == "get_current_weather"


def test_assistant_content_is_valid_json() -> None:
    row = {
        "prompt": "ignore me",
        "completion": {"tool": None, "reason": "out of scope"},
    }
    msgs = to_messages(row)
    parsed = json.loads(msgs[2]["content"])
    assert parsed["tool"] is None
    assert parsed["reason"] == "out of scope"
