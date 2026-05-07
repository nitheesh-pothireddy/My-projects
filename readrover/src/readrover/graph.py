"""LangGraph workflow definition.

This is the orchestration layer that wires sub-agents into a state machine:

    START
      │
      ▼
    search_planner ──────────────┐
      │                          │
      ▼                          │
    pdf_reader                   │
      │                          │
      ▼                          │
    critic ────[findings_weak]───┘   (re-plan up to max_iterations)
      │ findings_strong
      ▼
    writer
      │
      ▼
     END

State is a Pydantic model so every node has a typed contract.
"""

from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from readrover.agents import critic, pdf_reader, search_planner, writer
from readrover.config import settings


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------


class Paper(BaseModel):
    """An arXiv paper retrieved for the current question."""

    arxiv_id: str
    title: str
    authors: list[str]
    abstract: str
    published: str
    pdf_url: str


class Chunk(BaseModel):
    """A chunk of paper text with provenance, ready to embed."""

    paper_id: str
    text: str
    page: int | None = None


class Finding(BaseModel):
    """A single supported claim distilled from retrieved chunks."""

    claim: str
    supporting_chunk_ids: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


class State(BaseModel):
    """The single mutable state object that flows through the graph."""

    # input
    question: str

    # search_planner outputs
    sub_questions: list[str] = Field(default_factory=list)
    search_queries: list[str] = Field(default_factory=list)

    # pdf_reader outputs
    papers: list[Paper] = Field(default_factory=list)
    chunks: list[Chunk] = Field(default_factory=list)

    # critic outputs
    findings: list[Finding] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    coverage_score: float = 0.0

    # writer output
    brief: str | None = None

    # control flow
    iteration: int = 0


# ---------------------------------------------------------------------------
# Conditional edges
# ---------------------------------------------------------------------------


def critic_router(state: State) -> Literal["search_planner", "writer"]:
    """Decide whether findings are strong enough to write, or we need to re-search."""
    if state.coverage_score >= 0.7:
        return "writer"
    if state.iteration >= settings.max_iterations:
        # Out of budget — write anyway with what we have.
        return "writer"
    return "search_planner"


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------


def build_graph() -> StateGraph:
    """Compose the LangGraph workflow.

    Returns a *compiled* graph ready for `.invoke({"question": "..."})`.
    """
    graph = StateGraph(State)

    graph.add_node("search_planner", search_planner.run)
    graph.add_node("pdf_reader", pdf_reader.run)
    graph.add_node("critic", critic.run)
    graph.add_node("writer", writer.run)

    graph.add_edge(START, "search_planner")
    graph.add_edge("search_planner", "pdf_reader")
    graph.add_edge("pdf_reader", "critic")
    graph.add_conditional_edges(
        "critic",
        critic_router,
        {"search_planner": "search_planner", "writer": "writer"},
    )
    graph.add_edge("writer", END)

    return graph.compile()
