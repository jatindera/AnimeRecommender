# backend/app/core/startup.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.recommender_service import RecommenderService
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)
settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.

    On startup:
      - Tries to preload the recommender (if Chroma DB exists)
      - If not found, logs a warning and continues gracefully.
    """
    try:
        mode = (settings.RAG_MODE or "AGENT").upper()
        try:
            RecommenderService.get_recommender(settings, mode)
            logger.info(f"✅ Startup warm-up complete in mode: {mode}")
        except FileNotFoundError:
            logger.warning(
                f"⚠️ No Chroma DB found at '{settings.CHROMA_DIR}'. "
                "Skipping warm-up. Please build vector store via /vector/create."
            )
        yield
    except Exception as e:
        logger.exception(f"❌ Startup initialization failed: {e}")
        raise
    finally:
        logger.info("👋 Shutting down Anime Recommender API...")
