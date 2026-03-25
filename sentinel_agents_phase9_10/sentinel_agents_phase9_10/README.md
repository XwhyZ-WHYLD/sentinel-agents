"""Sentinel Agents Phase 9 & 10
===============================

This directory contains an isolated milestone snapshot of the Sentinel Agents
runtime extended with **Phase 9** (deployment) and **Phase 10**
(self‑governance).  It builds upon the evaluation and governance layers
introduced in earlier phases and demonstrates how to add deployment
orchestration and self‑adaptation capabilities to the agent.

Overview
--------

The Sentinel Agents project is a governed, constraint‑first runtime for
autonomous AI agents.  Prior phases introduced the core runtime, secure
execution, risk assessment, swarm coordination, persistent memory,
adaptive learning, evaluation and governance.  This snapshot adds two
more layers:

* **Phase 9 – Deployment:**  A minimal deployment layer that
  orchestrates the runtime across multiple nodes and exposes a
  configuration system.  It introduces a `DeploymentManager` that
  reads configuration data and can be extended to support API gateways
  and multi‑node execution.

* **Phase 10 – Self‑Governance:**  A self‑governance layer that
  monitors evaluation results and risk scores to adapt policies
  automatically.  A `SelfGovernanceEngine` can adjust the policy
  engine's blocked keywords or risk thresholds based on observed
  behaviour, enabling the system to evolve its own constraints.

Usage
-----

Install dependencies and launch the FastAPI application:

```bash
pip install fastapi uvicorn pydantic
uvicorn sentinel_agents.api.main:app --reload
```

Send a POST request to `/execute` with a JSON body containing a
`task` field to see the full lifecycle in action.  The response
includes evaluation metrics and the deployment layer will produce a
deployment message.  Self‑governance updates will adjust the policy
over time.

Structure
---------

```
sentinel_agents_phase9_10/
└── sentinel_agents/
    ├── agent/              # Runtime and loader
    ├── api/                # FastAPI interface
    ├── capabilities/       # External tool stubs
    ├── deployment/         # Phase 9 deployment layer
    ├── evaluation/         # Phase 7 evaluation layer
    ├── governance/         # Phase 8 audit & governance layer
    ├── learning/           # Phase 6 adaptive learning layer
    ├── memory/             # Persistent memory store
    ├── policy/             # Policy enforcement
    ├── risk/               # Risk scoring engine
    ├── sandbox/            # Secure execution wrappers
    ├── self_governance/    # Phase 10 self‑governance layer
    └── swarm/              # Multi‑agent coordination (placeholder)
```

Limitations
-----------

The deployment and self‑governance layers in this snapshot are
intentionally simple and meant to illustrate integration points.  The
deployment manager reads a static configuration and logs deployment
events without actually orchestrating containers or nodes.  The
self‑governance engine uses a heuristic to add new blocked keywords
when risk is non‑zero.  These modules provide hooks for more
sophisticated orchestration, policy evolution and meta‑reasoning in
future iterations.
"""