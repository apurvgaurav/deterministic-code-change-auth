# Deterministic Code Change Authorization System

**Forces every code change to prove itself before it gets merged.**

This is an execution-based authorization system, not a probabilistic suggestion tool.

---

## What This System Does
- Replays code changes under controlled execution  
- Compares behavior against a trusted reference  
- Enforces deterministic authorization decisions  

---

## Outputs
- ✅ ALLOW — behavior verified  
- ❌ BLOCK — behavior diverges  
- ⚫ UNVERIFIABLE — cannot prove correctness  

---

## Demo
Demo will be added here.

---

## Why Now

As AI systems increasingly generate code, the volume of changes is outpacing human review capacity. This creates a gap where correctness is assumed, not verified.

This system introduces a deterministic authorization layer to ensure code changes are proven under execution before being allowed.

This shift becomes critical as code generation scales faster than human validation capacity.

---

## Decision Boundary

- ALLOW → behavior is provably equivalent  
- BLOCK → behavior diverges  
- UNVERIFIABLE → determinism is insufficient  

The system prioritizes provable correctness over coverage.

---

## Comparison

| System | What it does | Core Limitation |
|--------|--------------|----------------|
| Static Analysis | Detects risky patterns | No execution-level proof |
| Tests | Validate predefined scenarios | Incomplete behavioral coverage |
| LLM Tools | Suggest fixes | Non-deterministic, non-reproducible |
| This System | Enforces execution equivalence | Requires reproducible environments |

---

## CI/CD Integration

PR → Tests → Replay Authorization → Merge Gate → Deploy

This system operates as a pre-merge authorization gate after tests but before deployment.

This transforms CI/CD from a validation pipeline into an enforcement pipeline.

---

## Controlled Evaluation

Evaluated on 36 controlled scenarios:

- 12 ALLOW  
- 12 BLOCK  
- 12 UNVERIFIABLE  

The objective was not to maximize approval rate, but to validate the integrity of the system’s decision boundary under controlled conditions.

---

## Early Failure Insight

In early iterations, normalization removed output differences that appeared non-critical but actually masked meaningful behavioral changes.

This introduced the risk of false ALLOW decisions.

The system was corrected by tightening the comparison surface and explicitly defining authoritative outputs, making it stricter but significantly more reliable.

---

## Where This System Should Not Be Used

- Highly non-deterministic systems  
- Distributed systems with external side effects  
- Real-time systems with strict latency constraints  
- Environments that cannot be reproduced  

This system is designed for correctness-critical paths, not universal enforcement.

---

## High-Stakes Example

In a financial system, a small change in rounding logic could silently alter transaction values while still passing tests.

This system would detect that behavioral divergence under replay and block the change before it reaches production.

---

## Final Positioning

This system does not attempt to guess correctness.

It enforces a simple rule:

If correctness cannot be proven under execution, the change is not allowed.
