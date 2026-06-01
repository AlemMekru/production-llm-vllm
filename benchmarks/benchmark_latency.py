import argparse
import statistics
import time
from typing import List

import requests


def percentile(values: List[float], percent: float) -> float:
    if not values:
        return 0.0

    sorted_values = sorted(values)
    index = int(round((percent / 100) * (len(sorted_values) - 1)))
    return sorted_values[index]


def run_benchmark(
    gateway_url: str,
    requests_count: int,
    message: str,
    model: str,
    temperature: float,
    max_tokens: int,
) -> None:
    endpoint = f"{gateway_url.rstrip('/')}/chat"

    latencies = []
    failures = 0

    print("Starting latency benchmark")
    print(f"Endpoint: {endpoint}")
    print(f"Requests: {requests_count}")
    print(f"Model: {model}")
    print("-" * 60)

    benchmark_start = time.perf_counter()

    for i in range(1, requests_count + 1):
        payload = {
            "message": message,
            "system_prompt": "You are a helpful AI assistant.",
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        request_start = time.perf_counter()

        try:
            response = requests.post(endpoint, json=payload, timeout=180)
            elapsed = time.perf_counter() - request_start

            if response.status_code == 200:
                latencies.append(elapsed)
                print(f"[{i}/{requests_count}] OK - {elapsed:.4f}s")
            else:
                failures += 1
                print(f"[{i}/{requests_count}] FAILED - HTTP {response.status_code}")

        except Exception as exc:
            failures += 1
            print(f"[{i}/{requests_count}] FAILED - {exc}")

    total_time = time.perf_counter() - benchmark_start
    successful = len(latencies)

    print("\nBenchmark Results")
    print("=" * 60)
    print(f"Total requests:       {requests_count}")
    print(f"Successful requests:  {successful}")
    print(f"Failed requests:      {failures}")
    print(f"Total time:           {total_time:.4f}s")

    if successful > 0:
        print(f"Average latency:      {statistics.mean(latencies):.4f}s")
        print(f"Minimum latency:      {min(latencies):.4f}s")
        print(f"Maximum latency:      {max(latencies):.4f}s")
        print(f"P50 latency:          {percentile(latencies, 50):.4f}s")
        print(f"P95 latency:          {percentile(latencies, 95):.4f}s")
        print(f"Requests/second:      {successful / total_time:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Latency benchmark for the Open-Weights LLM Inference Gateway."
    )

    parser.add_argument(
        "--gateway-url",
        default="http://127.0.0.1:8000",
        help="FastAPI gateway URL",
    )

    parser.add_argument(
        "--requests",
        type=int,
        default=10,
        help="Number of requests to send",
    )

    parser.add_argument(
        "--message",
        default="Explain what this project demonstrates to an AI hiring manager.",
        help="Prompt message",
    )

    parser.add_argument(
        "--model",
        default="meta-llama/Llama-3.1-8B-Instruct",
        help="Model name",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature",
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum output tokens",
    )

    args = parser.parse_args()

    run_benchmark(
        gateway_url=args.gateway_url,
        requests_count=args.requests,
        message=args.message,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
