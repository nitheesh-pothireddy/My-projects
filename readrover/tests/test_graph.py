"""Tests for state shapes and graph wiring (no LLM calls)."""

from __future__ import annotations

import pytest

from readrover.graph import State, build_graph, critic_router


def test_state_defaults(initial_state: State) -> None:
    assert initial_state.question.startswith("What is")
    assert initial_state.papers == []
    assert initial_state.chunks == []
    assert initial_state.findings == []
    assert initial_state.brief is None
    assert initial_state.iteration == 0


def test_critic_router_routes_to_writer_when_coverage_high(initial_state: State) -> None:
    initial_state.coverage_score = 0.9
    assert critic_router(initial_state) == "writer"


def test_critic_router_routes_to_search_when_coverage_low(initial_state: State) -> None:
    initial_state.coverage_score = 0.3
    initial_state.iteration = 0
    assert critic_router(initial_state) == "search_planner"


def test_critic_router_breaks_loop_when_iteration_budget_exhausted(
    initial_state: State,
) -> None:
    initial_state.coverage_score = 0.3
    initial_state.iteration = 99  # well past max_iterations
    assert critic_router(initial_state) == "writer"


def test_graph_compiles() -> None:
    """The graph should compile without raising."""
    graph = build_graph()
    assert graph is not None


def test_graph_has_expected_nodes() -> None:
    """All four sub-agents should be registered."""
    graph = build_graph()
    expected = {"search_planner", "pdf_reader", "critic", "writer"}
    actual = set(graph.nodes.keys()) - {"__start__", "__end__"}
    assert expected.issubset(actual)
