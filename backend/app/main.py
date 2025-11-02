# backend/app/main.py
from fastapi import FastAPI

# Import lifespan and routers
from app.core.startup import lifespan
from app.routes import health_router, recommend_router, vector_router

# ------------------------------------------------------------------------------
# FastAPI Application Initialization
# ------------------------------------------------------------------------------

app = FastAPI(
    title="Anime Recommender API",
    version="1.0.0",
    lifespan=lifespan,  # Handles startup/shutdown events
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
