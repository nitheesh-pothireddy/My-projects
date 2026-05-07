"""Critic agent.

Responsibility:
    For each sub-question:
      1. Retrieve top-K relevant chunks from the vector store.
      2. Have the LLM extract claims (Findings) grounded in those chunks.
      3. Score how well the sub-questions are *covered* (0.0 - 1.0).
      4. Detect contradictions: surface pairs of claims that disagree.

Inputs:  state.sub_questions, state.chunks (already embedded)
Outputs: state.findings, state.contradictions, state.coverage_score

Why this matters:
    The Critic is what makes ReadRover an *agent* and not a pipeline.
    By scoring coverage and conditionally re-routing back to the planner
    (see graph.critic_router), you get an actual loop with a stopping
    condition, which is the core LangGraph signal you want on your resume.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from readrover.graph import State


def run(state: "State") -> dict:
    """Extract findings, score coverage, surface contradictions."""
    # TODO(nitheesh): implement.
    #   1. vs = VectorStore(collection=hash(state.question))
    #   2. for sq in state.sub_questions:
    #          chunks = vs.query(sq, k=settings.top_k_chunks)
    #          findings += llm_extract_findings(sq, chunks)
    #   3. coverage = llm_score_coverage(state.sub_questions, findings)
    #   4. contradictions = llm_find_contradictions(findings)
    #   return {"findings": findings,
    #           "contradictions": contradictions,
    #           "coverage_score": coverage}
    raise NotImplementedError("Implement critic.run — see docstring TODO.")
