---
title: Atomic Notes
type: concept
tags: [pkm, writing]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Atomic Notes

One note holds one idea, nameable in a noun phrase and readable in under two minutes.

## Why it matters

Note size determines what a link can mean. If notes are documents, `[[Machine Learning]]`
tells you almost nothing — the target contains forty ideas and the link points at all of
them. If notes are single ideas, a link is a specific claim about a specific relationship,
and the graph becomes a structure you can reason over instead of decoration. Atomicity is
not a tidiness preference; it is what makes [[Link As Assertion]] possible.

## Detail

Three operational tests, in order of how often they fire:

- **The naming test.** If you cannot name the note in a noun phrase without "and", it is
  two notes. "Caching and Rate Limits" is a folder pretending to be a page.
- **The heading test.** A section called "Miscellaneous" or "Other notes" means the
  boundary is wrong — that content belongs somewhere else, or nowhere.
- **The length test.** Past roughly 400 lines, split and leave a hub note behind. This is
  the weakest test and the easiest to check, which is why the linter enforces it and not
  the other two.

The opposite failure is real and less discussed: notes so small they are just a
definition with no claim attached. A vault of two hundred one-line stubs has a beautiful
graph and says nothing. This is what `status: seed` is for — it marks a note as a
placeholder that caught a link, honestly labelled, so a maintenance pass can find it and
either grow it or merge it away.

> [!inference] The 400-line threshold is a convention chosen for this vault, not a
> finding from the source material. It is a place to start, not a claim about ideal note
> length.

## Connections

- [[Link As Assertion]] — the practice atomicity exists to enable
- [[Self-Evolving Wiki]] — the vault whose sizing rule this is
- [[Agentic Ingestion Loop]] — applies this test when deciding what earns a page
