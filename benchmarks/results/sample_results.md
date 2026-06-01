# Sample Benchmark Results

These results were collected in local mock mode on a Mac development machine.

Mock mode validates the FastAPI gateway, request flow, metrics collection, and benchmark script. Real GPU benchmark results will be added after deployment to a vLLM server.

## Local Mock Mode

| Metric | Value |
|---|---:|
| Total requests | 10 |
| Successful requests | 10 |
| Failed requests | 0 |
| Total time | 0.1776s |
| Average latency | 0.0176s |
| Minimum latency | 0.0078s |
| Maximum latency | 0.0588s |
| P50 latency | 0.0133s |
| P95 latency | 0.0588s |
| Requests/second | 56.3169 |

## Notes

- Provider: mock
- Gateway: FastAPI
- Frontend: Streamlit
- Model label: meta-llama/Llama-3.1-8B-Instruct
- These are not real model inference results.
- Real vLLM GPU metrics will include latency, throughput, tokens/sec, concurrency, and GPU memory usage.
