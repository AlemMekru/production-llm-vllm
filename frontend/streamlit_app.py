import time
import requests
import streamlit as st


GATEWAY_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Open-Weights LLM Gateway",
    page_icon="🧠",
    layout="wide",
)


st.title("🧠 Open-Weights LLM Inference Gateway")
st.caption("vLLM + FastAPI + Streamlit demo for self-hosted open-weights LLM serving")


with st.sidebar:
    st.header("Model Settings")

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

    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful AI assistant.",
        height=120,
    )

    st.divider()

    st.subheader("Domain Demo")

    demo_mode = st.selectbox(
        "Use-case preset",
        [
            "General Assistant",
            "Canadian Housing Decision Support",
            "Canadian Study Assistant",
            "Data-Sovereignty Explanation",
        ],
    )

    preset_prompts = {
        "General Assistant": "You are a helpful AI assistant.",
        "Canadian Housing Decision Support": (
            "You are an AI assistant supporting Canadian housing decision-support workflows. "
            "You explain rental affordability, housing stress signals, and rental-risk indicators in plain language. "
            "You do not make final housing decisions. You support human review and explain structured model outputs."
        ),
        "Canadian Study Assistant": (
            "You are an AI study assistant for Canadian learners. "
            "You explain concepts clearly, generate practice questions, and support study-mode learning."
        ),
        "Data-Sovereignty Explanation": (
            "You are an AI infrastructure assistant. "
            "You explain open-weights LLM deployment, self-hosting, vLLM, API gateways, and data-sovereignty-oriented architecture."
        ),
    }

    selected_system_prompt = preset_prompts[demo_mode]


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

    if st.button("Check vLLM Models"):
        try:
            response = requests.get(f"{GATEWAY_URL}/models", timeout=10)
            if response.status_code == 200:
                st.success("vLLM server is reachable.")
                st.json(response.json())
            else:
                st.warning("vLLM server is not reachable yet.")
                st.json(response.json())
        except Exception as exc:
            st.warning(f"vLLM is not running yet: {exc}")


if "messages" not in st.session_state:
    st.session_state.messages = []


for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])


user_message = st.chat_input("Ask the self-hosted model something...")

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
        with st.spinner("Calling FastAPI gateway..."):
            start_time = time.perf_counter()

            try:
                response = requests.post(
                    f"{GATEWAY_URL}/chat",
                    json=payload,
                    timeout=180,
                )

                elapsed = time.perf_counter() - start_time

                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data["response"]

                    st.markdown(assistant_message)

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Gateway latency", f"{data['latency_seconds']}s")
                    col2.metric("Input chars", data["input_chars"])
                    col3.metric("Output chars", data["output_chars"])

                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_message}
                    )
                else:
                    st.error("The gateway returned an error.")
                    st.code(response.text)

            except Exception as exc:
                st.error("Could not complete the request.")
                st.code(str(exc))
