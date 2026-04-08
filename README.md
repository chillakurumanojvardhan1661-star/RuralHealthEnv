# 🏥 RuralHealthEnv (v0.2.0)

### A Conversational OpenEnv Benchmark for Rural Healthcare Decision-Making in India

---

## 🚀 Overview

**RuralHealthEnv** is a realistic, OpenEnv-compliant reinforcement learning environment that simulates **conversational healthcare decision-making in rural India**. 

In version 0.2.0, the environment has been transformed into a **voice-call assistant simulation**, where an AI agent interacts with patients through natural language to guide medical decisions.

It enables AI agents to learn how to:

* ask relevant follow-up questions to extract clinical info
* assess patient urgency from dialogue
* decide between local treatment and referral
* operate under severe **resource constraints** in a conversational context

---

## 🇮🇳 Motivation

Rural healthcare in India faces critical challenges:

* ❌ No structured triage system
* 🚑 Emergency conditions often misjudged over phone calls
* 🏥 Limited access to hospitals and specialists
* 🌍 Resource constraints (no ICU, limited medicines, staff shortages)

---

## 🧠 Environment Design

### 🔁 OpenEnv API

The environment implements:

* `reset()` → initializes a new patient case and provides the first utterance.
* `step(action)` → processes natural language actions and returns `(observation, reward, done, info)`.
* `state()` → returns full internal state.

---

### 📥 Observation Space (Conversational)

```json
{
  "patient_info": { "age": 45, "gender": "male" },
  "symptoms": ["discovered_symptom_1"],
  "vitals": { "temperature": 98.6, "bp": "140/90", "heart_rate": 110 },
  "available_resources": ["PHC", "basic_medicines"],
  "distance_to_hospital": 25,
  "latest_utterance": "I have been shivering and having high fever...",
  "conversation_history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "extracted_data": { "symptoms": [...], "vitals": [...] }
}
```

---

### 🎯 Action Space

```json
{
  "action_type": "ask_question | classify_urgency | treat | refer | wait",
  "content": "Natural language response or question",
  "details": { "urgency": "low|medium|high" }
}
```

---

### 🎁 Conversational Reward Function

Multi-component, per-turn reward:

| Component            | Weight | Description |
| -------------------- | ------ | ----------- |
| Question Quality     | 0.2    | Relevance of follow-up questions |
| Information Gain     | 0.2    | Success in extracting symptoms |
| Triage Accuracy      | 0.3    | Correctness of urgency classification |
| Decision Correctness | 0.3    | Correctness of final Treat/Refer action |
| Safety               | 0.2    | Avoiding catastrophic patient progression |
| Resource Awareness   | 0.2    | Proper use of available facilities |

**Penalties:**
* ❌ Redundant question → -0.1
* ❌ Premature decision → -0.2
* ❌ Unsafe action → -0.5

---

## 🧩 Tasks

### 🟢 Easy — Urgency Classification
* Classify urgency from the initial patient description.
* **Dialogue**: 0 turns allowed.

### 🟡 Medium — Limited Interaction
* Ask 1-2 clarifying questions before making a decision.
* **Target**: Balance accuracy with speed.

### 🔴 Hard — Full Conversation Pipeline
* Full clinical dialogue (Max 8 turns).
* Agent must ask high-quality questions to "unlock" hidden risks before deciding.

---

## 🧪 Simulation Logic

### 🗣️ Dynamic Patient Response
Patients generate realistic rural Indian responses to agent questions. They may be vague or omit information unless asked correctly.

### 🧠 Information Extraction Layer
Simulates the agent's ability to parse speech into structured clinical data. As the conversation progresses, the `symptoms` list in the observation is updated.

---

## 🧪 Inference System

Run the multi-turn conversational agent:

```bash
python3 inference.py
```

### 📊 Output Format (Strict)

```
[START] task=hard env=RuralHealthEnv model=gpt-4-turbo
[STEP] step=1 action=ask_question reward=0.40 done=false error=null
[STEP] step=2 action=classify_urgency reward=0.30 done=true error=null
[END] success=true steps=2 rewards=0.40,0.30
```

---

## 🐳 Deployment

```bash
docker build -t rural-health-env .
docker run rural-health-env
```

---

## 📦 Project Structure

```
env/
 ├── environment.py       # Core OpenEnv Interaction
 ├── models.py            # Pydantic Schemas
 ├── state.py             # State & Dialogue History
 ├── reward.py            # Conversational Reward Logic
 ├── progression.py       # Patient Health Logic
 ├── patient_generator.py # 10+ Templates & Response Engine
 ├── nlp_utils.py         # Simulated Info Extraction
 ├── tasks/               # Multi-difficulty Task Suite
 └── graders/             # Deterministic Evaluation
inference.py             # Main Conversational LLM Loop
openenv.yaml             # Environment Config (v0.2.0)
Dockerfile               # Containerization
requirements.txt         # Dependencies
```

---

## 📜 License

MIT License
