from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    system_prompt: Optional[str] = Field(
        default="You are a helpful AI assistant.",
        description="Optional system prompt"
    )
    model: Optional[str] = Field(default=None, description="Model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1, le=4096)


class ChatResponse(BaseModel):
    model: str
    response: str
    latency_seconds: float
    input_chars: int
    output_chars: int
