from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

from gateway.schemas import ChatRequest, ChatResponse
from gateway.services.vllm_client import send_chat_completion, check_vllm_health
from gateway.config import DEFAULT_MODEL, VLLM_BASE_URL, LLM_PROVIDER


app = FastAPI(
    title="Open-Weights LLM Inference Gateway",
    description="FastAPI gateway for serving open-weights LLMs through vLLM.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "project": "Open-Weights LLM Inference Gateway",
        "status": "running",
        "provider": LLM_PROVIDER,
        "default_model": DEFAULT_MODEL,
        "vllm_base_url": VLLM_BASE_URL,
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gateway": "running",
        "provider": LLM_PROVIDER,
        "vllm_base_url": VLLM_BASE_URL,
    }


@app.get("/models")
async def models():
    try:
        return await check_vllm_health()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"vLLM server is not reachable: {str(exc)}"
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await send_chat_completion(
            message=request.message,
            system_prompt=request.system_prompt or "You are a helpful AI assistant.",
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return result
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"vLLM request failed: {str(exc)}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(exc)}"
        )
