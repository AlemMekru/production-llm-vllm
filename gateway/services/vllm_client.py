import time
from typing import Optional

import httpx

from gateway.config import (
    LLM_PROVIDER,
    RUNPOD_ENDPOINT_ID,
    RUNPOD_API_KEY,
    VLLM_BASE_URL,
    VLLM_API_KEY,
    DEFAULT_MODEL,
    REQUEST_TIMEOUT_SECONDS,
)


def build_mock_response(message: str) -> str:
    return (
        "This is a mock local response from the Open-Weights LLM Inference Gateway.\n\n"
        "Your FastAPI gateway and Streamlit UI are working correctly. "
        "When a GPU-hosted vLLM server is connected, this response will come from the real open-weights model.\n\n"
        f"User message received: {message}"
    )


async def send_chat_completion(
    message: str,
    system_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> dict:
    selected_model = model or DEFAULT_MODEL
    start_time = time.perf_counter()

    if LLM_PROVIDER == "mock":
        text = build_mock_response(message)
        latency = time.perf_counter() - start_time

        return {
            "model": f"{selected_model} (mock mode)",
            "response": text,
            "latency_seconds": round(latency, 4),
            "input_chars": len(message),
            "output_chars": len(text),
        }
    
    if LLM_PROVIDER == "runpod":
        payload = {
            "input": {
                "prompt": (
                    f"{system_prompt}\n\n"
                    f"Answer the user's question directly and briefly.\n"
                    f"Do not ask follow-up questions.\n\n"
                    f"User: {message}\n"
                    f"Assistant:"
                ),
                "sampling_params": {
                    "max_tokens": min(max_tokens, 25),
                    "temperature": 0,
                    "stop": ["\nUser:", "\nAssistant:", "User:", "Assistant:"],
                },
            }
        }

        headers = {
            "Authorization": f"Bearer {RUNPOD_API_KEY}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.post(
                f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/runsync",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        latency = time.perf_counter() - start_time

        text = ""
        try:
            text = data["output"][0]["choices"][0]["tokens"][0].strip()
            for marker in [
                "Bookmark",
                "You can also",
                "Search for",
                "Advertisement",
                "End of conversation",
                "Note:",
                "User:",
                "Assistant:",
                "Is there anything else",
                "Would you like",
            ]:
                if marker in text:
                    text = text.split(marker)[0].strip()

            if text.endswith(".") is False and len(text) > 0:
                text = text + "."
        except Exception:
            text = str(data)

        return {
            "model": selected_model,
            "response": text,
            "latency_seconds": round(latency, 4),
            "input_chars": len(message),
            "output_chars": len(text),
        }    

    payload = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    headers = {
        "Authorization": f"Bearer {VLLM_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.post(
            f"{VLLM_BASE_URL}/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()

    latency = time.perf_counter() - start_time
    text = data["choices"][0]["message"]["content"]

    return {
        "model": selected_model,
        "response": text,
        "latency_seconds": round(latency, 4),
        "input_chars": len(message),
        "output_chars": len(text),
    }


async def check_vllm_health() -> dict:
    if LLM_PROVIDER == "mock":
        return {
            "provider": "mock",
            "status": "mock mode active",
            "message": "vLLM server is not required in mock mode.",
            "default_model": DEFAULT_MODEL,
        }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"{VLLM_BASE_URL}/models")
        response.raise_for_status()
        return response.json()
