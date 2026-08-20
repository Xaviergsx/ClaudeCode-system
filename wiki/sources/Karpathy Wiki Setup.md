---
title: Karpathy Wiki Setup
type: source
tags: [pkm, agents, meta/map]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Karpathy Wiki Setup

Source note for the description of Andrej Karpathy's Claude-plus-markdown setup, the
document this vault was bootstrapped from.

## Summary

The setup pairs [[Claude Code]] with a local folder of markdown files, usually viewed
through [[Obsidian]], to produce what the source calls a "self-evolving LLM wiki". Raw
material lands in `raw/`; the agent reads it and writes interlinked pages into `wiki/`;
a root `CLAUDE.md` constrains the agent's behavior; `index.md` and `log.md` give it a map
of its own memory and a record of what it has done. The pitch is that this replaces a
vector database with plain text that an agent maintains, cross-links, and lints over
time.

## Claims worth keeping

> [!quote] "It replaces complex vector databases with plain text files that Claude
> maintains, cross-links, and 'lints' autonomously over time."

- **Four components carry the design.** `raw/` for capture, `wiki/` for structure,
  `CLAUDE.md` for governance, `index.md` + `log.md` for navigation and audit. Everything
  else in this vault is elaboration on those four. See [[Self-Evolving Wiki]].
- **Governance is a file, not a habit.** The behavioral rules — think first, edit
  surgically, don't over-engineer — live in `CLAUDE.md` where the agent rereads them every
  session, rather than in prompts that get forgotten. See [[Context Engineering]].
- **Retrieval becomes navigation.** The source argues plain text beats embeddings for
  personal knowledge because the agent traverses a structure it built itself, which is
  legible and diffable, instead of doing nearest-neighbour lookup over opaque vectors.
  See [[Navigation Over Retrieval]].
- **The viewer is disposable.** Obsidian renders the graph and nothing depends on it; the
  vault is a folder of text files that survives any tool change.

## Instructions as given

1. Create a clean directory with `raw/` and `wiki/` subfolders.
2. Add `CLAUDE.md` with strict execution constraints.
3. Run `claude` from inside the folder.
4. Prompt the agent to read raw files, structure them into interconnected nodes, update
   the index, and maintain the wiki iteratively.

Step 4 is the part this vault turns into a defined operation rather than an ad-hoc
prompt — see [[Agentic Ingestion Loop]].

## Open

> [!open] The source asserts that plain text beats vector search for this use case but
> gives no threshold. At what vault size does grep-and-navigate stop working? Tracked in
> [[Navigation Over Retrieval]].

## Connections

- [[Self-Evolving Wiki]] — the pattern this document describes, written up on its own terms
- [[Andrej Karpathy]] — the person the setup is attributed to
- [[Knowledge Systems]] — the map this note sits under
