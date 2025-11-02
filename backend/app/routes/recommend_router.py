# backend/app/routes/recommend_router.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import RecommendRequest, RecommendResponse
from app.services.recommender_service import RecommenderService
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)
settings = Settings()
router = APIRouter()

@router.post("", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    """Generate anime recommendations based on input query and mode."""
    try:
        mode = (req.mode or settings.RAG_MODE or "AGENT").upper()
        recommender = RecommenderService.get_recommender(settings, mode)
        answer = recommender.recommend(req.question)
        return RecommendResponse(mode=mode, answer=answer or "")
    except Exception as e:
        logger.exception("❌ Recommendation failed")
        raise HTTPException(status_code=500, detail=str(e))
