# Open-Weights LLM Inference Gateway for Canadian AI Applications

Production-style open-weights LLM inference gateway using **vLLM**, **FastAPI**, **Streamlit**, **Docker**, and benchmark-ready architecture.

This project demonstrates practical AI engineering skills beyond API usage: model-serving architecture, backend integration, provider abstraction, local development mode, Docker-based deployment, and readiness for latency/throughput benchmarking.

---

## Project Status

| Component                  | Status           |
| -------------------------- | ---------------- |
| FastAPI Gateway            | Working          |
| Streamlit UI               | Working          |
| Mock LLM Provider          | Working          |
| vLLM Provider              | Deployment-ready |
| Docker Compose             | Added            |
| Benchmark Scripts          | Planned          |
| Real GPU Benchmark Results | Pending          |

---

## Architecture

```text
User
  ↓
Streamlit UI
  ↓
FastAPI Gateway
  ↓
LLM Provider Layer
  ├── Mock Provider for local development
  └── vLLM OpenAI-compatible server for GPU inference
        ↓
Open-weights model: Llama 3.1 8B Instruct
```

---

## What This Project Demonstrates

* Self-hosted open-weights LLM architecture
* Production-style FastAPI gateway design
* Streamlit-based chat interface
* Provider abstraction for mock and vLLM backends
* OpenAI-compatible vLLM integration path
* Docker Compose deployment structure
* Environment-based configuration
* Readiness for latency, throughput, and concurrency benchmarking
* Practical AI infrastructure documentation for hiring managers and technical reviewers

---

## Technology Stack

| Layer         | Technology              |
| ------------- | ----------------------- |
| LLM Serving   | vLLM                    |
| Model         | Llama 3.1 8B Instruct   |
| API Gateway   | FastAPI                 |
| Frontend      | Streamlit               |
| HTTP Client   | httpx / requests        |
| Configuration | python-dotenv           |
| Deployment    | Docker / Docker Compose |
| Language      | Python                  |

---

## Repository Structure

```text
production-llm-vllm/
│
├── README.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.gateway
├── Dockerfile.frontend
├── .env.example
│
├── gateway/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── services/
│       └── vllm_client.py
│
├── frontend/
│   └── streamlit_app.py
│
├── benchmarks/
│   ├── benchmark_latency.py
│   ├── benchmark_concurrency.py
│   └── results/
│       └── sample_results.md
│
├── scripts/
│   ├── run_vllm_fp16.sh
│   ├── run_vllm_awq.sh
│   └── run_load_test.sh
│
└── docs/
    ├── architecture.md
    ├── deployment.md
    └── optimization.md
```

---

## Local Development Mode

The project includes a mock LLM provider so the full application can run locally without a GPU.

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create local environment file

```bash
cp .env.example .env
```

For local development, use:

```env
LLM_PROVIDER=mock
```

### 4. Run the FastAPI gateway

```bash
uvicorn gateway.main:app --reload --port 8000
```

Gateway:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 5. Run the Streamlit UI

Open a second terminal:

```bash
cd production-llm-vllm
source .venv/bin/activate
streamlit run frontend/streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

## vLLM Deployment Mode

For real open-weights model serving, switch the provider from mock mode to vLLM mode.

In `.env`:

```env
LLM_PROVIDER=vllm
VLLM_BASE_URL=http://localhost:8001/v1
VLLM_API_KEY=EMPTY
DEFAULT_MODEL=meta-llama/Llama-3.1-8B-Instruct
REQUEST_TIMEOUT_SECONDS=120
```

For gated Hugging Face models such as Llama, set:

```env
HUGGING_FACE_HUB_TOKEN=your_token_here
```

The included Docker Compose configuration uses:

```text
vllm/vllm-openai:latest
```

---

## Docker Deployment

The project includes separate Dockerfiles for the API gateway and frontend.

### Build and run

```bash
docker compose up --build
```

Expected services:

| Service         | URL                      |
| --------------- | ------------------------ |
| FastAPI Gateway | http://localhost:8000    |
| Streamlit UI    | http://localhost:8501    |
| vLLM Server     | http://localhost:8001/v1 |

Note: Real vLLM inference requires a compatible Linux GPU environment with NVIDIA CUDA support. On a Mac, use mock mode for local development.

---

## API Endpoints

| Method | Endpoint  | Description                              |
| ------ | --------- | ---------------------------------------- |
| GET    | `/`       | Project metadata                         |
| GET    | `/health` | Gateway health check                     |
| GET    | `/models` | vLLM model check or mock provider status |
| POST   | `/chat`   | Chat completion request                  |

### Example `/chat` request

```json
{
  "message": "Explain this project to a Canadian AI hiring manager.",
  "system_prompt": "You are a helpful AI assistant.",
  "model": "meta-llama/Llama-3.1-8B-Instruct",
  "temperature": 0.7,
  "max_tokens": 512
}
```

### Example mock response

```json
{
  "model": "meta-llama/Llama-3.1-8B-Instruct (mock mode)",
  "response": "This is a mock local response from the Open-Weights LLM Inference Gateway...",
  "latency_seconds": 0.0,
  "input_chars": 63,
  "output_chars": 334
}
```

---

## Performance Summary

Real GPU benchmark results will be added after deployment to a GPU server.

| Setup        | Model                 | Quantization | Concurrent Users | Avg Latency | P95 Latency | Tokens/sec | GPU Memory |
| ------------ | --------------------- | ------------ | ---------------: | ----------: | ----------: | ---------: | ---------: |
| Local Dev    | Mock Provider         | N/A          |                1 |       ~0.0s |         N/A |        N/A |        N/A |
| GPU Baseline | Llama 3.1 8B Instruct | FP16         |              TBD |         TBD |         TBD |        TBD |        TBD |
| Optimized    | Llama 3.1 8B Instruct | AWQ/FP8      |              TBD |         TBD |         TBD |        TBD |        TBD |

---

## Planned Benchmark Metrics

The next phase will add benchmark scripts for:

| Metric                  | Description             |
| ----------------------- | ----------------------- |
| Average latency         | Mean response time      |
| P50 latency             | Median response time    |
| P95 latency             | Tail latency under load |
| Tokens per second       | Output generation speed |
| Requests per second     | Throughput              |
| Concurrent users        | Load handling capacity  |
| GPU memory usage        | Hardware efficiency     |
| Quantization comparison | FP16 vs AWQ or FP8      |

---

## Why This Project Matters

Many AI demos only call hosted APIs. This project demonstrates the engineering work required to serve an open-weights model through a controlled backend architecture.

It shows practical understanding of:

* LLM serving infrastructure
* Backend API gateway design
* Local and production provider separation
* Deployment preparation
* Runtime configuration
* Benchmark-oriented development
* Open-weights AI system design

---

## Portfolio Positioning

This project is designed to complement other AI portfolio projects such as:

* RAG systems
* NLP classification projects
* AI decision-support platforms
* Domain-specific AI applications

Together, these show both application-level AI development and infrastructure-level LLM deployment capability.

---

## Author

**Alem Mekru**
MSc Artificial Intelligence
Senior Software Engineer
GitHub: [alemmekru](https://github.com/alemmekru)
