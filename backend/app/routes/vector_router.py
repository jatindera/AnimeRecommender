# backend/app/routes/vector_router.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import BuildResponse
from app.services.vector_service import VectorService
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)
settings = Settings()
router = APIRouter()

@router.post("/create", response_model=BuildResponse)
def create_vector_store():
    """Rebuilds the Chroma vector store using the configured CSV file."""
    try:
        result = VectorService.build_vector_store(
            raw_csv=settings.RAW_CSV_PATH,
            chroma_dir=settings.CHROMA_DIR,
            settings=settings,
        )
        logger.info("✅ Vector store created successfully.")
        return BuildResponse(**result)
    except Exception as e:
        logger.exception("❌ Vector store build failed")
        raise HTTPException(status_code=500, detail=str(e))
