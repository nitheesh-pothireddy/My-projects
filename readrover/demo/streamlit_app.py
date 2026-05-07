"""ReadRover Streamlit demo — drop a question, watch the agent work."""

from __future__ import annotations

import streamlit as st

from readrover.config import settings
from readrover.graph import build_graph

st.set_page_config(
    page_title="ReadRover",
    page_icon="🦫",
    layout="wide",
)

st.title("🦫 ReadRover")
st.caption(
    "Multi-agent research assistant. Ask a question, get a citation-backed brief "
    "synthesized from arXiv papers."
)

with st.sidebar:
    st.header("Settings")
    settings.top_k_papers = st.slider("Papers to read", 3, 10, settings.top_k_papers)
    settings.max_iterations = st.slider("Max re-plan loops", 1, 4, settings.max_iterations)
    st.markdown(
        "**Model:** `" + settings.model + "`  \n"
        "**Embeddings:** `" + settings.embedding_model + "`"
    )

question = st.text_input(
    "Your research question",
    placeholder="What's the state of small-model reasoning in 2026?",
)

if st.button("Run", type="primary", disabled=not question):
    with st.status("Running ReadRover...", expanded=True) as status:
        st.write("→ Planning sub-questions...")
        st.write("→ Fetching arXiv papers...")
        st.write("→ Embedding chunks...")
        st.write("→ Critic + synthesis...")

        try:
            graph = build_graph()
            final_state = graph.invoke({"question": question})
            status.update(label="Done", state="complete")
        except NotImplementedError as e:
            st.error(
                "An agent is still a stub. Implement `agents/*.py` first.\n\n" f"Detail: {e}"
            )
            st.stop()

    brief = final_state.get("brief", "")
    if brief:
        st.markdown("---")
        st.markdown(brief)

        with st.expander("Sources"):
            for paper in final_state.get("papers", []):
                st.markdown(f"- **[{paper.title}]({paper.pdf_url})** — {', '.join(paper.authors)}")
    else:
        st.warning("No brief produced.")
