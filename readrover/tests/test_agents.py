"""Tests for individual sub-agents.

Until you implement the agents these will mostly be xfail — that's expected.
Each agent should have at least 2 unit tests once implemented:
  - happy path with a fake LLM response
  - edge case (empty input, malformed LLM output, etc.)
"""

from __future__ import annotations

import pytest

from readrover.agents import critic, pdf_reader, search_planner, writer
from readrover.graph import State


@pytest.mark.xfail(reason="search_planner not yet implemented", strict=True)
def test_search_planner_produces_sub_questions(initial_state: State) -> None:
    out = search_planner.run(initial_state)
    assert "sub_questions" in out
    assert 2 <= len(out["sub_questions"]) <= 4


@pytest.mark.xfail(reason="pdf_reader not yet implemented", strict=True)
def test_pdf_reader_returns_papers(initial_state: State) -> None:
    initial_state.search_queries = ["small model reasoning 2025"]
    out = pdf_reader.run(initial_state)
    assert len(out["papers"]) > 0


@pytest.mark.xfail(reason="critic not yet implemented", strict=True)
def test_critic_emits_coverage_score(initial_state: State) -> None:
    out = critic.run(initial_state)
    assert 0.0 <= out["coverage_score"] <= 1.0


@pytest.mark.xfail(reason="writer not yet implemented", strict=True)
def test_writer_produces_markdown(initial_state: State) -> None:
    out = writer.run(initial_state)
    assert "brief" in out
    assert "##" in out["brief"]  # has at least one section header
