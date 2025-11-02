# backend/app/services/vector_service.py
import os
import shutil
import time
from dataio.data_loader import AnimeDataLoader
from rag.vector_store import VectorStoreBuilder
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VectorService:
    """Handles Chroma DB creation and maintenance."""

    @staticmethod
    def clear_chroma(chroma_dir: str) -> None:
        """
        Delete existing Chroma DB folder if it exists.
        Safe to call even if directory doesn't exist.
        """
        start = time.time()
        try:
            if os.path.exists(chroma_dir):
                logger.info(f"🧹 Clearing existing Chroma DB at: {chroma_dir}")
                shutil.rmtree(chroma_dir)
                logger.info(f"✅ Cleared Chroma DB in {round(time.time() - start, 2)}s.")
            else:
                logger.debug(f"No existing Chroma DB found at {chroma_dir}.")
        except Exception as e:
            logger.exception(f"❌ Failed to clear Chroma DB: {e}")

    @staticmethod
    def build_vector_store(raw_csv: str, chroma_dir: str, settings) -> dict:
        """
        Rebuild the Chroma vector database.

        Steps:
        1. Clear existing Chroma DB directory.
        2. Load and process anime dataset.
        3. Build vector store from processed data.
        """
        start_time = time.time()
        logger.info("🚀 Starting vector store build...")

        try:
            # Step 1: Cleanup
            VectorService.clear_chroma(chroma_dir)

            # Step 2: Load and process data
            loader = AnimeDataLoader(raw_csv)
            processed_file = loader.load_and_process()
            logger.info(f"✅ Processed data saved to: {processed_file}")

            # Step 3: Create vector store
            builder = VectorStoreBuilder(processed_file, settings)
            builder.create_vector_store()

            duration = round(time.time() - start_time, 2)
            logger.info(f"🎉 Vector store successfully built in {duration}s.")
            return {"status": "success", "seconds": duration}

        except Exception as e:
            logger.exception(f"❌ Vector store build failed: {e}")
            raise
