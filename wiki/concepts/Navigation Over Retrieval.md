---
title: Navigation Over Retrieval
type: concept
tags: [pkm, agents, ai/rag]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Navigation Over Retrieval

The claim that an agent traversing a structure it built itself beats similarity search
over embeddings, for a personal knowledge base.

## Why it matters

This is the argument that justifies the whole setup. If it is wrong, the correct design
is a vector database and the markdown is just a viewer. It is worth stating precisely
enough to be falsifiable rather than accepted as folklore.

## Detail

The argument, as the source makes it: retrieval-augmented generation over embeddings does
nearest-neighbour lookup in an opaque space. You cannot inspect why a chunk was returned,
you cannot correct it, and the corpus never improves. Navigating a wiki instead means
reading `index.md`, following explained links, and grepping — all operations over a
structure that is legible, diffable, and portable, and that gets better each time the
agent passes over it.

What actually carries the argument, on inspection, is less "text beats vectors" than:

- **The structure is authored, not derived.** Chunk boundaries come from an ingestion
  loop that read the whole document and decided what mattered — see
  [[Agentic Ingestion Loop]] — rather than from a character-count splitter.
- **Errors are addressable.** A wrong link can be fixed and stays fixed. A bad retrieval
  can only be worked around.
- **The corpus compounds.** Merging, splitting, and promotion have no equivalent in an
  embedding store, where the only operation is adding more.

> [!open] The scaling limit is unaddressed. Grep-and-navigate is clearly fine at a
> hundred notes and clearly insufficient at a hundred thousand; nobody names where it
> breaks, or whether a well-maintained `index.md` pushes the threshold far enough that it
> never matters in practice.

> [!inference] The two approaches are probably not exclusive — embeddings over an
> agent-curated wiki would inherit the authored structure. No evidence either way in the
> source.

## Connections

- [[Self-Evolving Wiki]] — the design this argument justifies
- [[Karpathy Wiki Setup]] — where the claim originates
- [[Atomic Notes]] — supplies the note boundaries that make navigation precise
