# Sentinel Agents
Constraint-first governed runtime for autonomous AI agents

## What it is
Sentinel Agents is a prototype runtime for agent execution under policy, risk, memory, and sandbox constraints.

## Current status
Implemented at prototype level:
- Core runtime
- Secure execution
- Risk intelligence
- Swarm coordination
- Memory layer
- Phase 6 adaptive learning scaffold

## Repo structure
- root modules = active integrated architecture
- sentinel_agents_phase3 = isolated milestone snapshot
- sentinel_agents_phase4 = isolated milestone snapshot
- sentinel_agents_phase6 = isolated milestone snapshot
- sentinel_agents_secure_execution = Phase 2 snapshot

## What Phase 6 adds
Phase 6 introduces an isolated adaptive learning scaffold:
- learning_engine
- feedback_loop
- adaptation

## How to run
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload


### Why this matters
Because the repo page already shows 14 commits, root runtime folders, and multiple phase folders, but the README is not explaining any of that. :contentReference[oaicite:1]{index=1}

---

## 2) Clarify the repo identity

Right now the repo shows both:
- root integrated modules like `agent`, `api`, `memory`, `policy`, `risk`, `sandbox`, `swarm`
- separate phase folders like `sentinel_agents_phase3`, `sentinel_agents_phase4`, `sentinel_agents_phase6`, and `sentinel_agents_secure_execution` :contentReference[oaicite:2]{index=2}

That creates ambiguity.

### Fix
Add a section in README called `Repo structure` and state plainly:

- **root/** = current integrated prototype
- **sentinel_agents_phaseX/** = archived milestone packages
- new work goes into root unless intentionally building an isolated release snapshot

### Optional cleanup
Either:
- keep the phase folders and move them under `archive/`
- or keep them at root but label them clearly as snapshots

My recommendation:  
**do not delete them yet**. Just organize them.

A cleaner target tree:

```text
sentinel-agents/
├── agent/
├── api/
├── memory/
├── policy/
├── risk/
├── sandbox/
├── swarm/
├── archive/
│   ├── sentinel_agents_phase3/
│   ├── sentinel_agents_phase4/
│   ├── sentinel_agents_phase6/
│   └── sentinel_agents_secure_execution/
├── README.md
└── requirements.txt
