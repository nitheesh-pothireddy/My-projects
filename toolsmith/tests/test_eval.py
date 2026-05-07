"""Eval scoring functions don't need a model — pure-function tests."""

from __future__ import annotations

from toolsmith.eval import score_one


def test_perfect_match(gold_current_weather: dict) -> None:
    scored = score_one(gold_current_weather, gold_current_weather)
    assert scored == {
        "valid_json": True,
        "schema_match": True,
        "args_correct": True,
        "hallucinated": False,
    }


def test_correct_refusal(gold_refusal: dict) -> None:
    pred = {"tool": None, "reason": "out of scope"}
    scored = score_one(pred, gold_refusal)
    assert scored["schema_match"]
    assert scored["args_correct"]
    assert not scored["hallucinated"]


def test_hallucinated_tool(gold_current_weather: dict) -> None:
    pred = {"tool": "get_uv_index", "arguments": {}}
    scored = score_one(pred, gold_current_weather)
    assert scored["hallucinated"]
    assert not scored["schema_match"]


def test_wrong_tool_not_flagged_as_hallucination(gold_current_weather: dict) -> None:
    pred = {"tool": "get_forecast", "arguments": {"latitude": 17.385, "longitude": 78.487}}
    scored = score_one(pred, gold_current_weather)
    assert not scored["hallucinated"]
    assert not scored["schema_match"]


def test_loose_lat_long_match(gold_current_weather: dict) -> None:
    """Geocoding precision shouldn't fail args_correct."""
    pred = {
        "tool": "get_current_weather",
        "arguments": {"latitude": 17.4, "longitude": 78.5, "temperature_unit": "celsius"},
    }
    scored = score_one(pred, gold_current_weather)
    assert scored["args_correct"]
