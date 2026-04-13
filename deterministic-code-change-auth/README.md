# Deterministic Code Change Authorization System

**Forces every code change to prove itself before it gets merged.**

## What This System Does
- Replays code changes in a controlled environment
- Compares behavior against a trusted reference
- Enforces deterministic merge decisions

## Outputs
- ALLOW
- BLOCK
- UNVERIFIABLE

## Demo
Demo will be added here.

## Why Now

As AI systems increasingly generate code, the volume of changes is outpacing human review capacity. This creates a gap where correctness is assumed, not verified.

This system introduces a deterministic authorization layer to ensure code changes are proven under execution before being allowed.

## Decision Boundary

- ALLOW → behavior is provably equivalent
- BLOCK → behavior diverges
- UNVERIFIABLE → determinism is insufficient

The system optimizes for decision integrity, not coverage.

## Comparison

| System | What it does | Limitation |
|--------|--------------|------------|
| Static Analysis | Detects risky patterns | No execution proof |
| Tests | Validate scenarios | Incomplete coverage |
| LLM Tools | Suggest fixes | Non-deterministic |
| This System | Enforces execution equivalence | Limited to reproducible environments |

## CI/CD Integration

PR → Tests → Replay Authorization → Merge Gate → Deploy

This system operates as a pre-merge authorization gate after tests but before deployment.

## Controlled Evaluation

Evaluated on 36 controlled scenarios:

- 12 ALLOW
- 12 BLOCK
- 12 UNVERIFIABLE

The goal was not to maximize approval rate, but to validate a strict decision boundary.

## Early Failure Insight

In early iterations, normalization removed output differences that appeared non-critical but actually masked meaningful behavioral changes.

This introduced the risk of false ALLOW decisions. The system was corrected by tightening the comparison surface and explicitly defining authoritative outputs.

## Where This System Should Not Be Used

- Highly non-deterministic systems
- Distributed systems with external side effects
- Real-time systems with strict latency constraints
- Environments that cannot be reproduced

This system is designed for correctness-critical paths, not universal enforcement.

## High-Stakes Example

In a financial system, a small change in rounding logic could silently alter transaction values while still passing tests.

This system would detect that behavioral divergence under replay and block the change before it reaches production.