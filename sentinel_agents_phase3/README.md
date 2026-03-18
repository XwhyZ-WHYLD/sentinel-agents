# Sentinel Agents (Working Title)

**Sentinel Agents** is a proof‑of‑concept framework for running autonomous AI agents **safely by default**.  It demonstrates a governed agent runtime with explicit capability permissions, a simple policy engine, and sandboxed execution.  The goal is to let agents take real actions (e.g. searching the web or reading files) while preventing them from doing anything outside the scope granted by their owner.

This repository contains an **MVP implementation** suitable for experimentation and learning.  It is *not* a complete production system, but it lays the groundwork for building a more robust, public‑safe agent platform in the future.

## ✨ Key concepts

- **Capability permissions** – Instead of loading arbitrary “skills” or plugins, each agent is granted a fixed set of capabilities (such as `search`, `read_file` or `http_fetch`).  Agents cannot call any tool they don’t have permission for.
- **Policy engine** – All tool calls are checked against a simple policy layer to deny dangerous actions (e.g. executing shell commands or accessing files outside a workspace).  This is where you can add custom risk controls.
- **Sandbox execution** – Agent actions run inside Docker containers so they cannot access the host machine.  Each task spawns a fresh container which is destroyed after execution.
- **Audit logging** – Every action the agent takes is logged with timestamp, agent name, requested tool and result.  This makes debugging and security review easier.

## 📦 Repository structure

```text
sentinel_agents
├── agent/
│   ├── runtime.py      # core agent runtime and planning loop
│   ├── planner.py      # simplistic task parser/decider
│   └── executor.py     # dispatches tool calls through policy engine
├── capabilities/
│   ├── search.py       # search API capability (stubbed)
│   ├── filesystem.py   # read/write to a restricted workspace
│   └── http_fetch.py   # simple HTTP GET requests
├── policy/
│   └── policy_engine.py # checks permissions and denies unsafe calls
    ├── risk/
    │   └── risk_engine.py  # computes risk scores for tool calls
├── sandbox/
│   ├── docker_runner.py    # spawns/destroys Docker containers for execution
│   ├── wasm_runner.py      # runs low‑risk tools in a Wasmtime sandbox
│   ├── firecracker_runner.py # runs high‑risk tools in a microVM
│   └── router.py           # chooses the appropriate sandbox for each call
├── api/
│   └── server.py       # FastAPI server exposing an endpoint to run an agent
└── README.md           # you are here
```

## 🚀 Quick start (development)

1. **Install dependencies.**  You’ll need Python 3.9+, Docker and pip.  From the project root:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   The MVP uses only standard libraries and [`fastapi`](https://fastapi.tiangolo.com/) / [`uvicorn`](https://www.uvicorn.org/) for the API server.

2. **Start the API.**

   ```bash
   uvicorn api.server:app --reload
   ```

3. **Call the agent.**  Send a JSON payload to `/run` specifying the agent name, prompt and allowed capabilities.  For example:

   ```bash
   curl -X POST http://localhost:8000/run \
        -H 'Content-Type: application/json' \
        -d '{
              "agent": "researcher",
              "prompt": "Find three recent papers on AI governance",
              "permissions": ["search", "http_fetch", "write_file"]
            }'
   ```

   The response includes the agent’s final answer and a list of audit log entries.  See `api/server.py` for details.

## ⚠️ Security note

This MVP is intentionally simple.  It does **not** include many of the protections required for production use:  there is no authentication or user isolation, the policy engine contains only a handful of rules, and the sandbox runner spawns containers on the same host.  You should treat this as a starting point for experimenting with governed agents, not a drop‑in solution for untrusted public deployment.

## 🔐 Phase 2 – Secure execution layer

The initial MVP ran all agent actions in a single Docker container on the host.  For any kind of public or semi‑trusted deployment, this isn’t enough.  The **secure execution layer** introduced in Phase 2 adds a **hybrid sandbox architecture** that chooses the most appropriate isolation technology for each capability call:

- **WASM sandbox (fast path)** – Safe, stateless tools (like simple API calls or data processing) are compiled to WebAssembly and executed in a Wasmtime runtime.  Startup time is measured in milliseconds and memory is tightly bounded.
- **Firecracker microVM (secure path)** – Potentially dangerous operations (reading or writing files, untrusted code execution) are run inside a Firecracker micro‑virtual machine.  This provides hardware‑level isolation at the cost of slightly higher latency.
- **Docker fallback (heavy path)** – Long‑running jobs or legacy executables can still run inside a standard Docker container when neither WASM nor microVM is suitable.

At runtime the agent’s executor asks the **sandbox router** (`sandbox/router.py`) to choose a sandbox type for every tool call.  The router uses a simple heuristic: file operations and anything with elevated risk go to Firecracker; safe API calls go to WASM; everything else falls back to Docker.  Each sandbox runner stub (`wasm_runner.py`, `firecracker_runner.py`, `docker_runner.py`) exposes a unified `run_in_sandbox(fn, *args, **kwargs)` API so the rest of the system doesn’t care about the underlying isolation.

Other improvements in Phase 2 include:

- **Network restrictions** –  Capability definitions can now specify allowed domains and whether to tunnel through a proxy.  All other outbound network requests are denied.
- **Resource limits** –  Each sandbox enforces CPU, memory and execution time limits to prevent runaway agents from exhausting host resources.
- **Audit logs** –  The log format now records the sandbox type used for each action, making it easier to trace how decisions were made.

These changes don’t magically make Sentinel Agents production‑ready, but they demonstrate how to evolve the MVP toward a public‑safe platform.  See `sandbox/router.py` for the routing logic and the new sandbox runner stubs in `sandbox/` for details.

## 🧠 Phase 3 – Risk & Policy Intelligence

Phase 3 introduces a **risk engine** and **intelligent policy enforcement**.  Instead of simply checking whether a tool call is permitted, the runtime now:

- **Scores every action.**  A new `risk` module assigns a risk score between 0.0 and 1.0 to each tool invocation based on its name and arguments.  File operations and non‑HTTPS network requests are considered high‑risk; simple searches are low‑risk.
- **Makes dynamic decisions.**  The sandbox router accepts a risk score and selects a sandbox accordingly.  Very low risk calls run in the WASM sandbox, medium‑risk calls run in Docker, and high‑risk calls go to Firecracker for maximum isolation.
- **Logs the why.**  Audit log entries now include the risk score and the chosen sandbox.  Denied calls record the risk and reason for denial.

The agent runtime uses a new helper (`executor.execute_with_policy`) to evaluate risk, consult the policy engine and route the call.  This brings Sentinel one step closer to a true *governed agent kernel* where every action is a decision, not a direct execution.

## 📚 Background

Sentinel Agents was inspired by the idea that autonomous AI systems must be governed by explicit policies and controlled capabilities.  Existing agent frameworks often prioritise feature richness over safety, leaving operators responsible for deploying and hardening them.  This MVP demonstrates a different approach:  **safety first**.  By constraining what an agent can do, adding an audit trail, and enforcing sandboxing, we hope to build a more trustworthy foundation for real‑world AI assistants.

## 🛠️ Contributing

Contributions are welcome!  Feel free to submit pull requests or open issues with suggestions.  Since this is an MVP, the code is intentionally small and easy to hack on.  We ask that all new capabilities pass through the policy engine and include tests.

---

*This README and the MVP code were originally generated with the assistance of an AI agent.*