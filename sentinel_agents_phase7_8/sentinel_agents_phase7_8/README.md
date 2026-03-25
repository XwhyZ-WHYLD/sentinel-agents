"""Sentinel Agents Phase 7 & 8
================================

This directory contains an *isolated milestone snapshot* of the Sentinel Agents
runtime extended with **Phase 7** (evaluation) and **Phase 8** (governance & audit).
It builds upon the architecture introduced in previous phases—core runtime,
policy, risk, memory, swarm and learning—and demonstrates how evaluation
metrics and audit logging can be integrated into the agent lifecycle.

Overview
--------

The Sentinel Agents project is a governed, constraint‑first runtime for
autonomous AI agents.  Prior phases introduced foundational layers:

* **Phase 1:** Core runtime loop
* **Phase 2:** Secure execution via sandboxing
* **Phase 3:** Risk scoring and classification
* **Phase 4:** Swarm coordination for multi‑agent workflows
* **Phase 5:** Persistent memory store
* **Phase 6:** Adaptive learning and feedback loop

This snapshot adds two new layers:

* **Phase 7 – Evaluation:**  Compute metrics on agent behaviour and
  provide simple regression testing.  An `EvaluationEngine` records
  whether an execution was successful and assigns a basic quality score.

* **Phase 8 – Governance & Audit:**  Capture audit traces of all
  executions for compliance and traceability.  A `GovernanceEngine`
  writes logs to disk via an `AuditLogger`.  This layer can later be
  extended to support traceability, policy explainability and external
  compliance hooks.

Usage
-----

To run the demonstration API for this phase, install the dependencies and
start the FastAPI server:

```bash
pip install fastapi uvicorn pydantic
uvicorn sentinel_agents.api.main:app --reload
```

Send a POST request to the `/execute` endpoint with a JSON body like
`{"task": "Tell me a fun fact about the ocean."}` to see the runtime in
action.  The response will include evaluation metadata and the audit
layer will append a log entry to `audit.log` in the current working
directory.

Structure
---------

```
sentinel_agents_phase7_8/
└── sentinel_agents/
    ├── agent/             # Runtime and loader
    ├── api/               # FastAPI interface
    ├── capabilities/      # External tool stubs
    ├── evaluation/        # Phase 7 evaluation layer
    ├── governance/        # Phase 8 audit & governance layer
    ├── learning/          # Phase 6 adaptive learning layer
    ├── memory/            # Persistent memory store
    ├── policy/            # Policy enforcement
    ├── risk/              # Risk scoring engine
    ├── sandbox/           # Secure execution wrappers
    └── swarm/             # Multi‑agent coordination (placeholder)
```

Limitations
-----------

This implementation is intentionally minimal.  The evaluation engine
computes only a single success/failure score and the governance layer
records only a basic audit log.  They are meant as scaffolding for more
advanced techniques such as statistical quality metrics, regression test
suites, fine‑grained traceability and compliance integrations.  Nonetheless
the code demonstrates clear integration points for these concerns
without polluting the core runtime.

"""