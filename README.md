# 🏥 RuralHealthEnv

### An OpenEnv Benchmark for Rural Healthcare Decision-Making in India

---

## 🚀 Overview

**RuralHealthEnv** is a realistic, OpenEnv-compliant reinforcement learning environment that simulates **healthcare decision-making in rural India**.

It enables AI agents to learn how to:

* assess patient urgency
* decide between local treatment and referral
* operate under severe **resource constraints**
* avoid unsafe or delayed medical decisions

> 🎯 This environment models real-world challenges faced by rural patients and frontline health workers, where incorrect decisions can lead to serious consequences.

---

## 🇮🇳 Motivation

Rural healthcare in India faces critical challenges:

* ❌ No structured triage system
* 🚑 Emergency conditions often misjudged
* 🏥 Limited access to hospitals and specialists
* 💊 Unsafe or inappropriate local treatments
* 🌍 Resource constraints (no ICU, limited medicines, staff shortages)

As a result, patients frequently experience:

* delayed care
* incorrect treatment
* preventable complications

---

## 💡 Our Contribution

RuralHealthEnv addresses these gaps by providing:

### ✅ A Real-World Simulation Environment

Captures **decision-making under constraints**, not ideal conditions.

### ✅ A Benchmark for AI Agents

Allows evaluation of LLMs and RL agents on:

* safety
* reasoning
* resource awareness

### ✅ Deterministic, Reproducible Evaluation

All tasks include **ground-truth graders** with normalized scoring.

---

## 🧠 Environment Design

### 🔁 OpenEnv API

The environment implements:

* `reset()` → initializes a new patient case
* `step(action)` → returns `(observation, reward, done, info)`
* `state()` → returns full internal state

---

### 📥 Observation Space

```json
{
  "patient_info": { "age": 45, "gender": "male" },
  "symptoms": ["chest pain", "sweating"],
  "vitals": { "temperature": 98.6, "bp": "140/90", "heart_rate": 110 },
  "available_resources": ["PHC", "basic_medicines"],
  "distance_to_hospital": 25,
  "history": []
}
```

---

### 🎯 Action Space

```json
{
  "action_type": "diagnose | treat | refer | wait",
  "details": {}
}
```

---

### 🎁 Reward Function

Multi-component, per-step reward:

| Component            | Weight |
| -------------------- | ------ |
| Triage Accuracy      | 0.3    |
| Decision Correctness | 0.3    |
| Safety               | 0.2    |
| Resource Awareness   | 0.2    |

Penalties:

* ❌ Unsafe action → -0.5
* ❌ Ignoring emergency → -0.7

---

## 🧪 Patient Simulation

* 10+ realistic case templates
* Severity levels: mild, moderate, severe
* Hidden risk factors (e.g., diabetes, hypertension)
* Noisy/missing data for realism

---

## 🔄 Condition Progression

Patient state evolves over time:

* ✔ Correct action → improvement
* ❌ Wrong action → worsening
* ⏳ No action → deterioration

Catastrophic failures (e.g., ignoring emergencies) terminate the episode.

---

## 🧩 Tasks

### 🟢 Easy — Urgency Classification

* Single-step task
* Classify: low / medium / high

### 🟡 Medium — Treat vs Refer

* Decide between:

  * local treatment
  * referral to higher facility
* Must consider resources and severity

### 🔴 Hard — Full Decision Pipeline

Agent must:

1. interpret symptoms
2. classify urgency
3. choose action
4. generate safe recommendation
5. adapt to uncertainty and progression

---

## ⚖️ Grader System

Each task includes a deterministic grader:

* Score range: **0.0 – 1.0**
* Partial scoring supported
* Evaluates:

  * correctness
  * safety
  * feasibility

Example:

* correct triage → 1.0
* near miss → 0.5
* unsafe → 0.0

---

## 🧪 Inference System

Run:

```bash
python inference.py
```

### 🔐 Required Environment Variables

```bash
export MODEL_NAME="your-model"
export HF_TOKEN="your-token"
```

---

### 📊 Output Format (Strict)

```
[START] task=easy env=RuralHealthEnv model=xxx
[STEP] step=1 action=... reward=0.30 done=false error=null
[END] success=true steps=1 rewards=0.30
```

✔ Fully compliant with evaluation requirements

---

## 🐳 Deployment

### Build Docker Image

```bash
docker build -t rural-health-env .
```

### Run Container

```bash
docker run rural-health-env
```

---

## 📦 Project Structure

```
env/
 ├── environment.py
 ├── models.py
 ├── state.py
 ├── reward.py
 ├── progression.py
 ├── patient_generator.py
 ├── tasks/
 ├── graders/

inference.py
openenv.yaml
Dockerfile
requirements.txt
```

---

## 📈 Baseline Performance

| Task   | Expected Success Rate |
| ------ | --------------------- |
| Easy   | ~80%                  |
| Medium | ~50%                  |
| Hard   | <30%                  |

---

## 🌍 Real-World Impact

This environment can be used to:

* evaluate AI safety in healthcare
* train decision-support systems
* simulate rural healthcare constraints
* benchmark LLM reasoning under uncertainty

> 🧠 It bridges the gap between AI capability and real-world healthcare needs.

---

## 🏆 Why This Matters

RuralHealthEnv is not just a simulation — it is a **benchmark for responsible AI in high-stakes environments**.

It encourages agents to be:

* safe
* practical
* resource-aware
* human-aligned

---

## 📜 License

MIT License

---

## 🙌 Acknowledgements

Built for OpenEnv-based evaluation of real-world AI agents.
