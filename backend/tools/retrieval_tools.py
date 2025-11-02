# tools/retrieval_tools.py
from langchain.tools import tool
from langchain_chroma import Chroma
from utils.logger import setup_logger
import logging

logger = setup_logger(__name__, level=logging.INFO)


def make_retrieve_context_tool(vector_store: Chroma):
    """
    Factory that returns a retrieval tool bound to a given vector_store.

    Uses `as_retriever()` interface (LangChain 1.0) for standardized retrieval.
    """

    # ✅ Step 1: Build retriever with fine-grained control
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
        )

    # ✅ Step 2: Define the actual tool callable
    @tool(response_format="content_and_artifact", return_direct=False)
    def retrieve_context(query: str):
        """Retrieve the most relevant anime context for the given query."""
        logger.info(f"[TOOL] retrieve_context -> {query}")

        # get_relevant_documents() is the standard retriever API
        docs = retriever.invoke(query)

        # join retrieved content for LLM consumption
        context = "\n\n".join(d.page_content for d in docs)

        # Return both raw text (for reasoning) and docs (for metadata)
        return f"Retrieved context:\n{context}", docs

    return retrieve_context
