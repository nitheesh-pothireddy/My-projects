"""Search Planner agent.

Responsibility:
    1. Decompose the user's research question into 2-4 focused sub-questions.
    2. Expand each sub-question into one or more arXiv search queries
       (boolean operators, author filters, year filters).

Inputs:  state.question
Outputs: state.sub_questions, state.search_queries

Implementation hint:
    - Use a single LLM call with structured output (Pydantic schema) so you
      get a typed list back, not free-form text.
    - Keep the prompt short and ask for the JSON schema explicitly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from readrover.graph import State


def run(state: "State") -> dict:
    """Decompose `state.question` into sub-questions + arXiv queries.

    Returns a partial state dict that LangGraph will merge.
    """
    # TODO(nitheesh): wire this up to Claude with structured output.
    #   Suggested approach:
    #     1. Define a Pydantic schema like
    #          class Plan(BaseModel):
    #              sub_questions: list[str]
    #              search_queries: list[str]
    #     2. Use ChatAnthropic(model=settings.model).with_structured_output(Plan)
    #     3. Prompt: "You are a research planner. Decompose: {question}.
    #                 Return 2-4 sub-questions and matching arXiv search queries."
    #     4. Return {"sub_questions": plan.sub_questions,
    #                "search_queries": plan.search_queries,
    #                "iteration": state.iteration + 1}
    raise NotImplementedError("Implement search_planner.run — see docstring TODO.")
