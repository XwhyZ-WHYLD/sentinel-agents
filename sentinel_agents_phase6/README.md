# Sentinel Agents – Phase 6: Adaptive Learning Layer

This folder contains the **Phase 6** implementation of the Sentinel Agents project.  
Phase 6 introduces an **adaptive learning layer** that sits between the existing modules (policy, risk, memory, agent runtime, swarm, sandbox and capabilities) and the rest of the system.  

## What is Phase 6?

Previous phases (1–5) laid the groundwork for a governed, multi‑agent AI runtime:

* **Phase 1** – core agent runtime
* **Phase 2** – secure execution (sandboxing)
* **Phase 3** – risk intelligence (risk scoring and validation)
* **Phase 4** – swarm intelligence (multi‑agent coordination)
* **Phase 5** – persistent memory layer (context recall)

Phase 6 builds on these foundations by adding **adaptive learning** and a **feedback loop**.  The goal is to enable agents to learn from their past actions, refine their behaviour over time and incorporate feedback into policy and memory.  This phase is designed to be modular and isolated from the previous phases—everything for Phase 6 lives in this folder.

## Directory layout

```
sentinel_agents_phase6/
├── README.md           – this file
└── sentinel_agents/
    ├── __init__.py
    ├── agent/
    │   ├── __init__.py
    │   └── runtime.py         – simplified agent runtime
    ├── api/
    │   ├── __init__.py
    │   └── main.py            – example FastAPI interface
    ├── capabilities/
    │   └── __init__.py
    ├── learning/
    │   ├── __init__.py
    │   ├── learning_engine.py – core adaptive logic
    │   ├── feedback_loop.py   – feedback integration
    │   └── adaptation.py      – adaptation algorithms
    ├── memory/
    │   ├── __init__.py
    │   └── memory.py          – simple persistent store
    ├── policy/
    │   ├── __init__.py
    │   └── policy_engine.py   – permission checks and updates
    ├── risk/
    │   ├── __init__.py
    │   └── risk_engine.py     – risk scoring stubs
    ├── sandbox/
    │   ├── __init__.py
    │   └── sandbox_router.py  – sandbox placeholder
    └── swarm/
        ├── __init__.py
        └── swarm_coordinator.py – multi‑agent coordinator
```

### Packaging

To package this phase as an archive, run the following command from the root of the repository:

```bash
zip -r sentinel_agents_phase6.zip sentinel_agents_phase6/
```

This ensures Phase 6 can be distributed or deployed independently of other phases.

### Usage

The code in this folder provides a minimal, illustrative example of how an adaptive learning layer can integrate with the existing Sentinel Agents architecture.  The `LearningEngine` monitors executions via the agent runtime, stores execution traces in the `memory` module and feeds insights back into the `policy` via the `FeedbackLoop`.  While the implementations provided here are intentionally simple, the interfaces are designed for extensibility.

To experiment with the API, run:

```bash
pip install fastapi uvicorn
uvicorn sentinel_agents.api.main:app --reload
```

Then send requests to the `/execute` endpoint with a JSON payload containing a `task` field.  The agent will process the task and pass execution outcomes to the learning layer.