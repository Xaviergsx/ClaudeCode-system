---
title: Agentic Ingestion Loop
type: concept
tags: [pkm, agents, workflow]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Agentic Ingestion Loop

The defined operation that moves one document from `raw/` into the wiki: read it whole,
write a source note, extract concepts and entities, enrich what already exists, update
the map, log it.

## Why it matters

"Prompt Claude to read your raw files and maintain the wiki" is the step everyone gets
wrong, because as a one-line instruction it produces a different result every time. Named
as a fixed sequence with a definition of done, it becomes repeatable — which is the only
way the vault stays coherent across hundreds of sessions run months apart.

## Detail

The sequence, in order, one raw file at a time:

1. **Read the whole file.** Summarizing from the first page is the single most common
   corruption of the vault, and it is invisible afterward.
2. **Write the source note** in `wiki/sources/` — summary, extracted claims, links out.
   This is the only place a raw document gets restated at length; concept notes reference
   it rather than repeating it.
3. **Extract concepts and entities.** Link if the note exists, stub it as `status: seed`
   if it doesn't. Prefer linking. Producing fifty stubs from one document means you are
   extracting nouns, not ideas.
4. **Enrich existing notes.** This is where value compounds: new material that sharpens
   or contradicts an old note edits that note. A contradiction gets `> [!open]` and a
   question note — never a silent overwrite. See
   [[How Should Contradictions Be Resolved]].
5. **Update `index.md`**, run the linter, append to `log.md`.

Two constraints keep it honest. **One file at a time, to completion** — a half-ingested
document leaves dangling stubs no one can distinguish from real ones. And **the raw file
is never edited**, so provenance survives every later reorganization.

The step-4 enrichment is what separates this from filing. A system that only creates new
notes per document is a filing cabinet with extra steps; one that revises old notes as
new evidence arrives is accumulating understanding.

## Connections

- [[Self-Evolving Wiki]] — the structure this loop maintains
- [[Atomic Notes]] — decides step 3's boundary: what earns its own page
- [[Link As Assertion]] — governs the links written in steps 2 and 3
- [[Claude Code]] — the agent that runs the loop, via `/ingest`
