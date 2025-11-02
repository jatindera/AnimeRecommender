# health_router.py
# backend/app/routes/health_router.py
from fastapi import APIRouter
from config.settings import Settings
from utils.logger import setup_logger

# Initialize
router = APIRouter()
logger = setup_logger(__name__)
settings = Settings()

@router.get("", tags=["Health"])
def health_check():
    """
    Simple health check endpoint.

    Returns the current environment, model configuration,
    and a generic OK status. Used by uptime monitors,
    load balancers, and deployment pipelines.
    """
    logger.debug("Health check requested.")
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "model": settings.MODEL_NAME,
    }
