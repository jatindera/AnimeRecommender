# backend/app/models/schemas.py
from typing import Optional, Literal
from pydantic import BaseModel, Field

# ------------------------------------------------------------------------------
# Request & Response Schemas
# ------------------------------------------------------------------------------

class RecommendRequest(BaseModel):
    """Request body for the /recommend endpoint."""

    question: str = Field(
        ...,
        description="User query or description of the type of anime to recommend.",
        example="Recommend anime similar to Attack on Titan with deep emotional themes."
    )
    mode: Optional[Literal["AGENT", "CHAIN"]] = Field(
        default=None,
        description="Execution mode: 'AGENT' (agentic reasoning) or 'CHAIN' (simple RAG chain).",
        example="AGENT"
    )


class RecommendResponse(BaseModel):
    """Response model for the /recommend endpoint."""

    mode: str = Field(..., description="Mode used for the recommendation process.")
    answer: str = Field(..., description="Generated recommendation result.")


class BuildResponse(BaseModel):
    """Response model for the /vector/create endpoint."""

    status: str = Field(..., description="Operation status (e.g., 'success').")
    seconds: float = Field(..., description="Execution time in seconds.")
