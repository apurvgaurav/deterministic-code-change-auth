# Deterministic Code Change Authorization System

A deterministic enforcement system for code change authorization.

This system does not suggest code.
It does not guess correctness.

It verifies whether a code change is valid — and returns an explicit **ALLOW** or **BLOCK** decision.

---

## Why this exists

Most modern code tools are probabilistic.

They generate outputs that *look correct*, but they don’t prove that they *are correct*.

That approach breaks down in:

* security-sensitive systems
* compliance-heavy environments
* audit-driven engineering workflows

This project enforces a stricter rule:

> A code change is accepted only if it can be deterministically verified.

---

## What this system does

This system evaluates a proposed code change through a deterministic pipeline:

1. Map the change to a known issue pattern
2. Apply a predefined remediation template (non-generative)
3. Generate a patch deterministically
4. Replay the change in a controlled execution environment
5. Compare outputs at the byte level
6. Return a final decision: **ALLOW** or **BLOCK**
7. Record the decision in an audit trail

No scoring. No probability. No partial correctness.

---

## Core principles

* deterministic execution only
* template-based remediation (non-generative)
* replay verification
* byte-level validation
* explicit ALLOW / BLOCK decision
* audit-first architecture
* reproducibility over probability

---

## System Flow

![Deterministic Pipeline](./docs/figures/system_flow.png)

End-to-end deterministic pipeline from input code to final authorization decision.

---

## Policy Gate

![Deterministic Policy Gate](./docs/figures/policy_gate.png)

A change proceeds only if it matches a known deterministic rule.

If no rule matches:

* no patch is generated
* no unsafe transformation is attempted
* the event is logged for audit

---

## Verification & Decision

![Replay Verification](./docs/figures/replay_verification.png)

The system replays the generated patch and compares outputs at the byte level.

* **R1 == R2 → ALLOW**
* **R1 ≠ R2 → BLOCK**

No probabilistic acceptance. No fallback heuristics.

---

## Why Not LLM-Based Fixing

![LLM vs Deterministic](./docs/figures/llm_vs_deterministic.png)

LLM-based systems generate code probabilistically.

This system enforces deterministic verification.

If a result cannot be reproduced exactly, it is rejected.

---

## Demo Behavior

This prototype demonstrates both core outcomes:

* **ALLOW** → replay match = true
* **BLOCK** → replay mismatch = detected

These are enforced decisions, not simulated scenarios.

---

## UI

Frontend includes:

* request input panel
* result view
* raw response output
* decision banner (ALLOW / BLOCK)
* replay mismatch toggle

---

## API

* `GET /health` → service status
* `POST /authorize` → evaluate code change

---

## Repository Structure

backend/
  app/
    api.py
    main.py
    core/

frontend/
  src/
    components/

docs/
  figures/

README.md

---

## Use Cases

* controlled code remediation pipelines
* policy-driven change authorization
* compliance-sensitive engineering environments
* audit-first software systems

---

## Current Status

* backend: complete
* frontend: complete
* deterministic pipeline: implemented end-to-end
* replay verification: working
* ALLOW / BLOCK logic: validated
* demo-ready system

---

## Disclosure Note

A non-provisional patent has been filed for this system and is currently under examination.

This repository intentionally presents system behavior and high-level architecture only.
Detailed implementation logic and certain internal components are not publicly disclosed.

---

## Summary

This is not a faster way to write code.

It is a stricter way to decide whether code should be accepted.

If a change cannot be verified, it does not pass.
