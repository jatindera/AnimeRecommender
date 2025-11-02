# backend/app/services/recommender_service.py
import os
from recommender.anime_recommender import AnimeRecommender
from utils.logger import setup_logger

logger = setup_logger(__name__)

class RecommenderService:
    """Manages cached AnimeRecommender instance."""

    _cached = {"mode": None, "rec": None}

    @classmethod
    def get_recommender(cls, settings, mode: str) -> AnimeRecommender:
        """Return cached AnimeRecommender instance, reinitialize if mode changes."""
        mode = mode.upper()
        os.environ["RAG_MODE"] = mode
        if cls._cached["rec"] and cls._cached["mode"] == mode:
            return cls._cached["rec"]

        rec = AnimeRecommender(settings=settings)
        cls._cached.update({"mode": mode, "rec": rec})
        logger.info(f"🔄 Initialized new recommender in mode: {mode}")
        return rec
