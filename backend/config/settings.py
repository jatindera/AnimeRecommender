# src/animerec/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):

    # Core configuration
    ENABLE_FILE_LOGGING: bool = Field(default=True)
    ENVIRONMENT: str = Field(default="local", description="Environment name: local, dev, prod, or azure")
    
    # Models
    MODEL_NAME: str = Field(default="gpt-4o-mini")  # or llama-3.1-8b-instant if using Groq
    EMBEDDING_MODEL: str = "text-embedding-3-large"  # or sentence-transformers

    # Stores
    CHROMA_DIR: str = "chroma_db"
    CHROMA_COLLECTION: str = "anime_collection"
    TOP_K: int = 3
    RAW_CSV_PATH: str = os.path.join("data", "anime_raw.csv")

    # Providers
    OPENAI_API_KEY: str | None = None

    # Others
    RAG_MODE: str = "AGENT"  # or CHAIN

    # CORS
    CORS_ALLOW_ORIGINS: str = Field(
        default="http://localhost,http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated list of allowed CORS origins",
    )

    class Config:
        env_file = ".env"
