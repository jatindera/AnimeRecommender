import argparse
import logging
import os
import shutil
import sys
import time

from config.settings import Settings
from dataio.data_loader import AnimeDataLoader
from recommender.anime_recommender import AnimeRecommender
from utils.logger import setup_logger
from rag.vector_store import VectorStoreBuilder

logger = setup_logger(__name__, level=logging.INFO)
settings = Settings()


# ---------------------------------------------------------
# 🧹 UTILS
# ---------------------------------------------------------
def clear_chroma_db(chroma_path: str):
    """Delete existing Chroma DB folder if it exists."""
    if os.path.exists(chroma_path):
        logger.info(f"🧹 Clearing existing Chroma DB at: {chroma_path}")
        shutil.rmtree(chroma_path)
        time.sleep(1)
    else:
        logger.debug(f"No existing Chroma DB found at {chroma_path}.")


# ---------------------------------------------------------
# 🧱 BUILD PIPELINE
# ---------------------------------------------------------
def build_pipeline():
    """
    Build vector store from raw dataset.
    Steps:
      1. Clear old Chroma DB
      2. Load & process dataset
      3. Create & persist new vector store
    """
    start_time = time.time()
    logger.info("🚀 Starting vector store build pipeline...")

    try:
        clear_chroma_db(settings.CHROMA_DIR)

        # Load and process the dataset
        loader = AnimeDataLoader(settings.RAW_CSV_PATH)
        processed_file = loader.load_and_process()
        logger.info(f"✅ Processed data saved to: {processed_file}")

        # Build the vector store
        builder = VectorStoreBuilder(processed_file, settings)
        builder.create_vector_store()

        elapsed = time.time() - start_time
        logger.info(f"✅ Vector store build completed in {elapsed:.2f}s!")

    except Exception as e:
        logger.exception(f"❌ Vector store build failed: {e}")
        sys.exit(1)


# ---------------------------------------------------------
# ⚡ QUERY PIPELINE
# ---------------------------------------------------------
def run_mode(question: str, rag_mode: str):
    """
    Run the recommender in a given RAG mode (AGENT / CHAIN).
    """
    os.environ["RAG_MODE"] = rag_mode.upper()
    logger.info(f"=== Running {rag_mode.upper()} Mode ===")

    try:
        recommender = AnimeRecommender(settings=settings)
        response = recommender.recommend(question)
        logger.info("🎯 Recommendation completed successfully.")
        return response
    except Exception as e:
        logger.exception(f"❌ Error during recommendation: {e}")
        return None


# ---------------------------------------------------------
# 🏁 ENTRY POINT
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Anime Recommender System Pipeline")
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build the Chroma vector store and exit.",
    )
    parser.add_argument(
        "--mode",
        choices=["AGENT", "CHAIN"],
        default=settings.RAG_MODE if hasattr(settings, "RAG_MODE") else "AGENT",
        help="Choose RAG mode: AGENT or CHAIN",
    )
    parser.add_argument(
        "--question",
        type=str,
        default="Recommend anime similar to Attack on Titan with deep psychological and emotional themes.",
        help="Question to query the recommender with.",
    )

    args = parser.parse_args()

    logger.info("=== Anime Recommender System (LangChain 1.0) ===")

    if args.build:
        logger.info("[MODE] BUILD MODE")
        build_pipeline()
        return

    logger.info(f"[MODE] QUERY MODE ({args.mode})")
    response = run_mode(args.question, args.mode)

    if response:
        print("\n[RECOMMENDER OUTPUT]\n")
        print(response)


if __name__ == "__main__":
    main()
