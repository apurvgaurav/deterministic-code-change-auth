# Deterministic Code Change Authorization System

A proof-based deployment control system that replaces review confidence with execution-verified evidence.

---

## What This System Does

Most deployment decisions rely on:

* static analysis
* test coverage
* human review

These infer behavior indirectly.

This system does something different:

→ It executes the change
→ Replays known scenarios
→ Produces a deterministic decision:

**ALLOW / BLOCK / UNVERIFIABLE**

No heuristics. No scoring. Only proof.

---

## Why This Matters

As code generation scales, review quality degrades.

This shifts the bottleneck from writing code → trusting it.

This system replaces inference with **direct behavioral verification**.

---

## Core Architecture

Pipeline:

1. Change Intake
2. Controlled Execution (Execution Capsule)
3. Deterministic Replay
4. Authorization Gate
5. Verified Release

The system introduces a **mandatory execution-verification boundary** before deployment.

---

## Example Outcome

| Scenario                     | Result       |
| ---------------------------- | ------------ |
| Parameterized SQL patch      | ALLOW        |
| Auth logic mutation          | BLOCK        |
| Non-deterministic dependency | UNVERIFIABLE |

---

## Replay Trace Snapshot

```text
Execution ID: EXEC-4B5477961BD9  
Environment Hash: 1ded43f3...  

Step 1: Execute candidate change  
Step 2: Capture state transitions  
Step 3: Replay expected trace  
Step 4: Compare outputs  

Result:
MATCH → ALLOW
```

---

## Running the System

```bash
git clone https://github.com/apurvgaurav/deterministic-code-change-auth
cd deterministic-code-change-auth
pip install -r requirements.txt
python -m app.main
```

---

## Repository Structure

```text
app/        → core execution + orchestration  
scripts/    → replay + validation utilities  
tests/      → scenario validation  
docs/       → system documentation  
```

---

## Demo

* System overview (~3.5 min): https://www.youtube.com/watch?v=7cPx0UJNquE
* Deep dive: https://www.youtube.com/watch?v=GL-GLeYNCOU

---

## Status

* Working prototype
* 36 controlled scenarios
* Non-provisional patent filed

---

## What This System Is Not

* Not an AI decision system
* Not probabilistic scoring
* Not a code suggestion tool

---

## Summary

This system introduces deterministic, execution-based authorization into the deployment pipeline.

It enforces proof where today we rely on interpretation.
