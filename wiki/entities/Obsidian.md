---
title: Obsidian
type: entity
tags: [tooling, pkm]
status: seed
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Obsidian

A local-first markdown editor that reads a folder of `.md` files as a vault, resolving
`[[wikilinks]]` and rendering the link structure as a graph.

## Why it matters

It is the viewer in this setup, and deliberately not a dependency. The vault is a folder
of text files; Obsidian makes the graph visible and backlinks cheap to browse, but
deleting it changes nothing about the content. Any editor, `grep`, or a future tool reads
the same files.

## Detail

Two features earn their place here: the graph view, which makes orphans and clusters
visible at a glance in a way the linter's text output cannot, and backlinks, which show a
note's inbound edges without leaving it. The `.obsidian/` directory holds app config only
and is excluded from the agent's writable surface.

## Connections

- [[Claude Code]] — writes the files this renders
- [[Self-Evolving Wiki]] — the vault this is a view onto
