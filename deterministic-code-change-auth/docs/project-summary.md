# Deterministic Code Authorization — Summary

## One-Line
Forces every code change to prove itself before it gets merged.

## Why Now
AI-generated code increases risk. Deterministic validation ensures correctness.

## Decision Model
ALLOW / BLOCK / UNVERIFIABLE

## Evaluation
36 controlled scenarios:
- 12 ALLOW
- 12 BLOCK
- 12 UNVERIFIABLE

## Failure Insight
Normalization initially masked real differences → fixed by tightening comparison boundary.

## Where It Breaks
- distributed systems
- non-deterministic outputs
- environment mismatch

## Positioning
Not a suggestion system.  
A deterministic authorization layer.