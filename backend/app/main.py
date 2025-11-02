# backend/app/main.py
from fastapi import FastAPI

# Import lifespan and routers
from app.core.startup import lifespan
from app.routes import health_router, recommend_router, vector_router
from fastapi.middleware.cors import CORSMiddleware
from config.settings import Settings

settings = Settings()

# ------------------------------------------------------------------------------
# FastAPI Application Initialization
# ------------------------------------------------------------------------------

app = FastAPI(
    title="Anime Recommender API",
    version="1.0.0",
    lifespan=lifespan,  # Handles startup/shutdown events
)

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------
allow_origins = [origin.strip() for origin in settings.CORS_ALLOW_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Include Routers
# ------------------------------------------------------------------------------

app.include_router(health_router.router, prefix="/health", tags=["Health"])
app.include_router(recommend_router.router, prefix="/recommend", tags=["Recommender"])
app.include_router(vector_router.router, prefix="/vector", tags=["Vector Store"])

# ------------------------------------------------------------------------------
# Entry Point for Local Development
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
