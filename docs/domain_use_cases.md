# Canadian AI Application Use Cases

This project is a general-purpose open-weights LLM inference gateway, but it is designed with Canadian AI applications in mind.

The goal is to demonstrate how a self-hosted or privately controlled LLM serving layer can support applications where API control, deployment flexibility, cost management, and data-governance considerations matter.

---

## 1. Canadian Housing Decision Support

This gateway can support housing-related AI systems such as rental search assistants, housing stress explanation tools, and rental-risk review workflows.

Example use cases:

- Explain rental affordability signals
- Summarize rental listing risks
- Generate plain-language explanations for housing stress scores
- Support human-in-the-loop rental decision workflows
- Provide natural-language explanations for ML model outputs

This aligns with AI decision-support concepts used in projects such as RentShield Canada, where machine learning and NLP components are used to support rental search, housing stress prediction, and risk explanation.

Important note: the LLM gateway is not designed to make final housing decisions. It is intended to support explanation, summarization, and user-facing interaction around structured model outputs.

---

## 2. Canadian Education and Study Applications

This gateway can also support educational AI features, including study assistants and exam-preparation tools.

Example use cases:

- Explain curriculum-aligned concepts
- Generate practice questions
- Provide study-mode explanations
- Support exam-mode answer review
- Power student-facing chat interfaces

This architecture supports applications where a frontend product needs controlled access to an LLM through a backend gateway instead of exposing model infrastructure directly.

---

## 3. Canadian Data-Sovereignty-Oriented AI

Many AI applications depend on external hosted APIs. This project demonstrates an alternative architecture where the application can connect to a privately hosted open-weights model.

Potential benefits:

- More control over inference infrastructure
- Reduced dependency on closed hosted APIs
- Ability to choose deployment region
- Clear separation between application layer and model-serving layer
- Better visibility into latency, throughput, and operational cost
- Easier integration with internal security and governance policies

This does not automatically guarantee data sovereignty. Actual data residency depends on where the vLLM server, logs, storage, monitoring, and backups are deployed. However, this architecture gives the application owner more control than a purely third-party hosted API design.

---

## 4. Public-Service and Community Information Assistants

A similar gateway can be used for public-service or community-support assistants.

Example use cases:

- Summarize public information
- Explain government or municipal resources in plain language
- Provide multilingual community support
- Route users to verified sources
- Support retrieval-augmented generation systems

For production systems, this should be combined with retrieval, source citation, guardrails, logging controls, and human review for high-impact use cases.

---

## Why These Use Cases Matter

The same LLM infrastructure can support multiple Canadian AI products:

- Housing decision-support tools
- Student study systems
- Community platforms
- Public-service assistants
- Internal enterprise AI copilots

The core engineering value of this project is the reusable serving layer:

```text
Application UI
  ↓
FastAPI Gateway
  ↓
Provider Layer
  ↓
vLLM / Open-Weights Model