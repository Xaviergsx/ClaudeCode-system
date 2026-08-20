---
title: Self-Evolving Wiki
type: concept
tags: [pkm, agents]
status: growing
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-wiki-setup.md]
---

# Self-Evolving Wiki

A folder of plain markdown that an agent maintains as its own long-term memory: it
ingests new material, files it into interlinked notes, and periodically reorganizes what
it already wrote.

## Why it matters

The usual answer to "give the model memory" is a vector database — chunk the documents,
embed them, retrieve by similarity. That works for question answering over a corpus and
poorly for a body of knowledge you want to *think with*, because nothing in it ever
improves. Chunks accumulate; they never get merged, corrected, or promoted. A wiki that
an agent edits has the opposite property: every pass over it can make it better, and the
improvements are visible in a diff.

## Detail

Four parts, and the discipline is in keeping it to four:

- **`raw/`** — immutable capture. Cheap to add to, never edited. This is what makes the
  system safe to be aggressive elsewhere: the agent can restructure `wiki/` freely
  because the ground truth is untouched.
- **`wiki/`** — atomic, interlinked notes. The agent's output and its working memory.
- **`CLAUDE.md`** — the governing rules, reread every session. See
  [[Context Engineering]].
- **`index.md` and `log.md`** — a flat map of everything, and an append-only record of
  what changed. The map is how the agent orients without reading every file; the log is
  how it — and you — audit what happened.

"Self-evolving" is doing real work as a description. The wiki is not just appended to; it
is *revised*. Notes get split when they grow two topics, merged when they say the same
thing, promoted from `seed` to `evergreen` when they earn it. That revision loop is the
difference between a knowledge base and a pile.

The failure mode is entropy that outruns curation: capture is cheap, structure is
expensive, and a vault that only ever ingests becomes a worse-organized version of the
`raw/` folder. This is why the maintenance pass in `CLAUDE.md` is a first-class operation
and not an afterthought.

## Connections

- [[Agentic Ingestion Loop]] — the operation that grows it
- [[Atomic Notes]] — the sizing rule that keeps the link graph informative
- [[Navigation Over Retrieval]] — the argument for why plain text is enough
- [[Karpathy Wiki Setup]] — the source this note was extracted from
