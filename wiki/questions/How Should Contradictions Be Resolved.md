---
title: How Should Contradictions Be Resolved
type: question
tags: [pkm, meta/process]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: []
---

# How Should Contradictions Be Resolved

When a new raw document contradicts a claim already written into a note, what should the
ingestion loop actually do?

## The problem

`CLAUDE.md` says: never silently overwrite, add a `> [!open]` block, raise a question
note. That is a safe default and not a resolution policy. It defers every conflict
forever, and a vault that accumulates unresolved contradictions is as unusable as one
that hides them.

## Options considered

- **Recency wins.** Newest source overwrites, old claim moves to a footnote. Cheap;
  wrong whenever the older source was better.
- **Source ranking.** Weight by source quality. Requires maintaining a ranking, which is
  its own contradiction-prone judgment.
- **Hold both, flag it.** Current behavior. Honest, but unbounded.
- **Hold both with an expiry.** Both claims stand, and the question note surfaces in the
  maintenance pass until a human decides. Adds a deadline to the current behavior.

## What would settle it

A rule for which conflicts an agent may resolve alone. A conflict about a fact with a
checkable answer is different from one about interpretation, and the vault currently
treats them identically.

## Connections

- [[Agentic Ingestion Loop]] — step 4 is where contradictions surface
- [[Self-Evolving Wiki]] — unresolved conflicts are the main way this design degrades
