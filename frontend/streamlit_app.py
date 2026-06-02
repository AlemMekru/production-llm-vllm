import time
import requests
import streamlit as st
import os

GATEWAY_URL = os.getenv(
    "GATEWAY_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="Canadian LLM Gateway",
    page_icon="🍁",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }

    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 45%, #991b1b 100%);
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .hero h1 {
        margin-bottom: 0.2rem;
        font-size: 2.1rem;
    }

    .hero p {
        margin: 0;
        font-size: 1.05rem;
        opacity: 0.95;
    }

    .info-card {
        padding: 1rem;
        border-radius: 14px;
        background: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 16px rgba(15,23,42,0.06);
        margin-bottom: 1rem;
    }

    .small-label {
        color: #64748b;
        font-size: 0.85rem;
        margin-bottom: 0.15rem;
    }

    .strong-value {
        color: #0f172a;
        font-size: 1rem;
        font-weight: 700;
    }

    .canada-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        background: #fee2e2;
        color: #991b1b;
        font-weight: 700;
        font-size: 0.85rem;
        margin-right: 0.4rem;
    }

    .muted {
        color: #64748b;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <span class="canada-badge">🍁 Canadian AI Infrastructure</span>
        <span class="canada-badge">RunPod + vLLM + Llama 3.1</span>
        <h1>Open-Weights LLM Inference Gateway</h1>
        <p>
            A production-style AI serving layer for Canadian applications:
            FastAPI gateway, Streamlit interface, RunPod Serverless inference, and Meta Llama 3.1 8B Instruct.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


top_col1, top_col2, top_col3, top_col4 = st.columns(4)

with top_col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="small-label">Model</div>
            <div class="strong-value">Llama 3.1 8B Instruct</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="small-label">Inference</div>
            <div class="strong-value">RunPod Serverless</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="small-label">Gateway</div>
            <div class="strong-value">FastAPI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_col4:
    st.markdown(
        """
        <div class="info-card">
            <div class="small-label">Frontend</div>
            <div class="strong-value">Streamlit</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.header("🍁 Gateway Controls")

    st.caption("Production-style LLM gateway for Canadian AI use cases.")

    model = st.text_input(
        "Model",
        value="meta-llama/Llama-3.1-8B-Instruct",
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
    )

    max_tokens = st.slider(
        "Max tokens",
        min_value=64,
        max_value=4096,
        value=512,
        step=64,
    )

    st.divider()

    st.subheader("🇨🇦 Domain Demo")

    demo_mode = st.selectbox(
        "Use-case preset",
        [
            "General Assistant",
            "Canadian Housing Decision Support",
            "Canadian Study Assistant",
            "Data-Sovereignty Explanation",
            "Public-Service Assistant",
        ],
    )

    preset_prompts = {
        "General Assistant": (
            "You are a concise, helpful AI assistant. "
            "Answer directly and avoid unnecessary follow-up questions."
        ),
        "Canadian Housing Decision Support": (
            "You are an AI assistant supporting Canadian housing decision-support workflows. "
            "Explain rental affordability, housing stress signals, and rental-risk indicators in plain language. "
            "Do not make final housing decisions. Support human review and explain structured model outputs."
        ),
        "Canadian Study Assistant": (
            "You are an AI study assistant for Canadian learners. "
            "Explain concepts clearly, generate practice questions, and support study-mode learning."
        ),
        "Data-Sovereignty Explanation": (
            "You are an AI infrastructure assistant. "
            "Explain open-weights LLM deployment, self-hosting, vLLM, API gateways, and data-sovereignty-oriented architecture."
        ),
        "Public-Service Assistant": (
            "You are a plain-language public-service AI assistant. "
            "Explain information clearly, avoid legal or medical advice, and encourage users to verify critical information with official sources."
        ),
    }

    selected_system_prompt = preset_prompts[demo_mode]

    st.info(f"Active preset: {demo_mode}")

    st.divider()

    st.subheader("Example Prompts")

    example_prompt = st.selectbox(
        "Try a prompt",
        [
            "",
            "What is the capital of Canada?",
            "Explain this project to a Canadian AI hiring manager.",
            "What does data sovereignty mean for Canadian AI applications?",
            "Explain housing stress in simple terms.",
            "Create three study questions about Canadian geography.",
        ],
    )

    st.divider()

    st.subheader("Gateway Health")

    if st.button("Check Gateway"):
        try:
            response = requests.get(f"{GATEWAY_URL}/health", timeout=10)
            if response.status_code == 200:
                st.success("FastAPI gateway is running.")
                st.json(response.json())
            else:
                st.error(f"Gateway error: {response.status_code}")
        except Exception as exc:
            st.error(f"Could not reach gateway: {exc}")

    if st.button("Check Provider"):
        try:
            response = requests.get(f"{GATEWAY_URL}/models", timeout=10)
            if response.status_code == 200:
                st.success("Provider check completed.")
                st.json(response.json())
            else:
                st.warning("Provider check returned a warning.")
                st.json(response.json())
        except Exception as exc:
            st.warning(f"Provider check failed: {exc}")


st.markdown(
    """
    <div class="info-card">
        <div class="strong-value">Live AI Gateway</div>
        <div class="muted">
            Ask a question below. Requests flow from Streamlit to FastAPI, then to the configured LLM provider.
            In production mode, this connects to RunPod Serverless running Meta Llama 3.1 8B Instruct.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = []


if example_prompt and not st.session_state.get("example_loaded"):
    st.session_state.example_loaded = True
    st.session_state.pending_prompt = example_prompt

if not example_prompt:
    st.session_state.example_loaded = False


for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])


default_prompt = st.session_state.pop("pending_prompt", "") if "pending_prompt" in st.session_state else ""

user_message = st.chat_input("Ask the Canadian LLM gateway something...")

if default_prompt and not user_message:
    user_message = default_prompt


if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.chat_message("user"):
        st.markdown(user_message)

    payload = {
        "message": user_message,
        "system_prompt": selected_system_prompt,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    with st.chat_message("assistant"):
        with st.spinner("Calling FastAPI gateway → RunPod Serverless → Llama 3.1..."):
            start_time = time.perf_counter()

            try:
                response = requests.post(
                    f"{GATEWAY_URL}/chat",
                    json=payload,
                    timeout=300,
                )

                elapsed = time.perf_counter() - start_time

                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data["response"]

                    st.markdown(assistant_message)

                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    metric_col1.metric("Gateway latency", f"{data['latency_seconds']}s")
                    metric_col2.metric("Client round trip", f"{elapsed:.2f}s")
                    metric_col3.metric("Input chars", data["input_chars"])
                    metric_col4.metric("Output chars", data["output_chars"])

                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_message}
                    )
                else:
                    st.error("The gateway returned an error.")
                    st.code(response.text)

            except Exception as exc:
                st.error("Could not complete the request.")
                st.code(str(exc))


st.divider()

st.caption(
    "Built by Alem Mekru · MSc Artificial Intelligence · Senior Software Engineer · "
    "Open-weights AI infrastructure for Canadian applications"
)