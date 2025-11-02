"""
anime_recommender.py — Core logic for the Anime Recommender System.

Supports two modes:
  - RAG_CHAIN: always retrieves context first (deterministic)
  - RAG_AGENT: lets the LLM decide when to use tools (agentic)

This module orchestrates model initialization, tool creation,
and streaming-based generation of recommendations.
"""

import logging
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

from utils.logger import setup_logger
from rag.vector_store import VectorStoreBuilder
from tools.retrieval_tools import make_retrieve_context_tool
from recommender.prompt_template import get_anime_prompt
from config.settings import Settings

logger = setup_logger(__name__, level=logging.INFO)


class AnimeRecommender:
    """Handles end-to-end anime recommendation using RAG Chain or RAG Agent."""

    def __init__(self, settings: Settings = Settings()):
        load_dotenv()
        self.settings = settings
        self.rag_mode = settings.RAG_MODE.upper()
        self.model = init_chat_model(settings.MODEL_NAME)

        # Load Chroma store using configured settings
        self.vector_store = VectorStoreBuilder(
            processed_csv="",  # not used here
            settings=settings
        ).load_vector_store()

        logger.info(f"AnimeRecommender initialized in {self.rag_mode} mode.")

        if self.rag_mode == "AGENT":
            self.agent = self._create_rag_agent()
        else:
            self.agent = self._create_rag_chain()

    # ---------------------------------------------------------
    # 🧠 RAG AGENT MODE
    # ---------------------------------------------------------
    def _create_rag_agent(self):
        """Agentic mode: LLM decides when/how to call retrieval tools."""
        retrieve_context = make_retrieve_context_tool(self.vector_store)
        tools = [retrieve_context]

        system_prompt = """
        You are an expert anime recommender agent.

        Your goal is to recommend the best anime titles for each user query.
        If you need more information, use the 'retrieve_context' tool to gather
        relevant anime details.

        Steps to follow:
        1. Understand user intent and preferences.
        2. Retrieve additional info if needed (via 'retrieve_context').
        3. Recommend 3 anime titles with:
           - A short summary (2–3 lines)
           - Why it matches user preferences
        4. Be factual, concise, and avoid fabricating data.
        """

        return create_agent(
            model=self.model,
            tools=tools,
            system_prompt=system_prompt,
        )

    # ---------------------------------------------------------
    # ⚡ RAG CHAIN MODE
    # ---------------------------------------------------------
    def _create_rag_chain(self):
        """Fixed pipeline mode: always retrieves before generating response."""

        @dynamic_prompt
        def prompt_with_context(request: ModelRequest) -> str:
            last_query = request.state["messages"][-1].text
            retrieved_docs = self.vector_store.similarity_search(last_query, k=3)
            context = "\n\n".join(doc.page_content for doc in retrieved_docs)
            template = get_anime_prompt()
            return template.format(context=context, question=last_query)

        return create_agent(self.model, tools=[], middleware=[prompt_with_context])

    # ---------------------------------------------------------
    # 🚀 RECOMMENDATION STREAMING
    # ---------------------------------------------------------
    def recommend(self, question: str) -> str:
        """Stream recommendations and log incremental updates."""
        logger.info(f"[QUERY] {question}")
        logger.info("[STREAMING OUTPUT START]")

        final_response = None
        last_text = ""

        for step in self.agent.stream(
            {"messages": [{"role": "user", "content": question}]},
            stream_mode="values",
        ):
            msg = step["messages"][-1]

            # 🛠️ Log tool calls
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                logger.info(f"Calling tools: {[tc['name'] for tc in msg.tool_calls]}")
                continue

            # ⚙️ Skip raw tool results
            if getattr(msg, "type", None) == "tool":
                continue

            # 💬 Print incremental text
            if getattr(msg, "type", None) == "ai" and getattr(msg, "content", None):
                new_text = msg.content[len(last_text):]
                if new_text.strip():
                    logger.info("")
                last_text = msg.content
                final_response = msg.content

        logger.info("[STREAMING OUTPUT END]")
        return final_response or "[No response generated]"
