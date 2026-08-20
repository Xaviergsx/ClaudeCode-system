---
title: Context Engineering
type: concept
tags: [agents, pkm, workflow]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Context Engineering

Shaping what an agent reads — file layout, naming, and a governing rules file — so that
correct behavior is the path of least resistance rather than something you re-request
every session.

## Why it matters

An agent's behavior is a function of its context window, and a session starts empty every
time. Rules given in chat evaporate; rules written into a file the agent reads on entry
persist. This is the load-bearing insight behind putting the constitution in `CLAUDE.md`
instead of in your prompting habits: the guardrails become part of the repository, so
they survive new sessions, new machines, and a different person at the keyboard.

## Detail

Three mechanisms do most of the work in this vault:

- **A governing file at the root.** `CLAUDE.md` holds boundaries, schema, and the
  definition of done. It is read before the first write, every session.
- **Structure that answers questions without reading files.** `index.md` lets the agent
  learn what exists for the cost of one file instead of a hundred. Explained links let it
  learn a neighbourhood from one section — see [[Link As Assertion]].
- **Names that carry meaning.** Globally unique `Title Case.md` filenames mean a link
  resolves without a path, and a `grep` for a concept finds the page rather than forty
  mentions.

The constraint that makes all three necessary: attention is finite and expensive. Every
design decision here trades vault-authoring effort for a cheaper agent read. That is also
the honest limit of the approach — it optimizes for an agent that reads and greps, and a
vault tuned this way is somewhat over-structured for a human browsing casually.

> [!inference] The source describes `CLAUDE.md` as dictating "agent boundaries" and
> "behavioral guardrails" but does not use the term context engineering. The framing here
> is this vault's, not the source's.

## Connections

- [[Self-Evolving Wiki]] — the system these techniques are applied to
- [[Link As Assertion]] — one concrete mechanism, written for agent legibility
- [[Claude Code]] — the agent whose context this shapes
