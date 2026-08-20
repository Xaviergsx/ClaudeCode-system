---
title: Link As Assertion
type: concept
tags: [pkm, writing]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Link As Assertion

Every link in this vault states why it exists. A bare `[[Target]]` is treated as an
incomplete sentence.

## Why it matters

A link graph built from bare links records that two notes are *somehow* related and
loses which way and why. That information was in the writer's head at the moment of
linking and is unrecoverable afterward — including by the agent, which is the reader that
matters most here. Writing `[[Transformers]] — RAG retrofits external memory onto them`
costs eight words and turns a topological edge into a claim you can check, argue with,
or discover is wrong.

## Detail

The rule: inside a `## Connections` section, every bullet is `[[Note]] — clause`, where
the clause explains the relationship rather than describing the target. "— is also about
caching" describes; "— is the failure mode this technique trades away" asserts.

Two consequences worth naming:

- **Links become falsifiable.** A stated reason can turn out to be wrong, which means a
  maintenance pass can actually find bad structure. Bare links never fail.
- **The graph reads as prose.** Opening a note and reading only its Connections section
  should teach you the neighbourhood. This is how an agent orients cheaply — it reads
  one section, not five notes. See [[Context Engineering]].

The cost is real: it makes linking slightly expensive, so fewer links get written. That
tradeoff is deliberate. A vault with forty explained links is more navigable than one
with four hundred unexplained ones.

## Connections

- [[Atomic Notes]] — the sizing rule that makes a single link specific enough to explain
- [[Context Engineering]] — why the explanation is written for an agent's benefit
- [[Agentic Ingestion Loop]] — the operation that must obey this rule when writing links
