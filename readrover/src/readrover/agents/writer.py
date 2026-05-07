"""Writer agent.

Responsibility:
    Synthesize the final markdown brief from the Critic's outputs.

The brief should:
    - Open with a 2-3 sentence TL;DR.
    - Have one section per sub-question.
    - Inline-cite findings as `[arxiv:1234.5678]`.
    - Have a dedicated "Where the literature disagrees" section
      pulled from state.contradictions.
    - End with a "Sources" section listing all papers used.

Inputs:  state.question, state.sub_questions, state.findings,
         state.contradictions, state.papers
Outputs: state.brief (markdown string)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from readrover.graph import State


def run(state: "State") -> dict:
    """Compose the citation-backed markdown brief."""
    # TODO(nitheesh): implement.
    #   Suggested prompt template (system + user):
    #     SYSTEM: "You are a research synthesiser. Output well-structured
    #              markdown. Cite every claim with [arxiv:<id>]. If sources
    #              disagree, note this explicitly."
    #     USER:   "Question: {question}\n
    #              Sub-questions: {sub_questions}\n
    #              Findings: {findings_with_chunk_text}\n
    #              Contradictions: {contradictions}\n
    #              Papers: {papers}"
    #   Use Anthropic streaming so the CLI feels responsive.
    raise NotImplementedError("Implement writer.run — see docstring TODO.")
