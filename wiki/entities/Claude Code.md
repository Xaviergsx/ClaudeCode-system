---
title: Claude Code
type: entity
tags: [agents, tooling]
status: seed
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Claude Code

Anthropic's agentic coding tool, run from a terminal inside a directory, where it can
read, search, and edit files directly. In this vault it is the maintainer: it runs the
ingestion loop and the maintenance passes.

## Why it matters

The setup depends on an agent with direct filesystem access rather than a chat window you
paste into. Reading a raw file, writing six notes, updating the index, and running the
linter is one uninterrupted operation — which is what makes a fixed loop possible at all.

## Detail

What this vault relies on: it reads `CLAUDE.md` on entry, so the rules apply without being
restated; it greps and reads selectively rather than loading everything; and the slash
commands in `.claude/commands/` turn the vault's operations into named verbs.

## Connections

- [[Agentic Ingestion Loop]] — the operation it runs here, via `/ingest`
- [[Context Engineering]] — how this vault is shaped for it specifically
- [[Obsidian]] — the other half of the pairing; renders what this writes
