# Index

The flat map of the brain. Every note in `wiki/`, one line each, grouped by type. This is
the file an agent reads first to learn what exists without opening a hundred files — so
it stays complete, and every entry earns its one-line description.

Last reconciled: 2026-08-20 · 13 notes

## Maps of content

- [[Home]] — the front door; every domain hangs off here
- [[Knowledge Systems]] — how this vault works and why plain text over a vector database

## Concepts

- [[Agentic Ingestion Loop]] — the fixed sequence that moves a document from `raw/` to `wiki/`
- [[Atomic Notes]] — one note, one idea; the sizing rule that makes links informative
- [[Context Engineering]] — shaping what the agent reads so good behavior is the default
- [[Link As Assertion]] — every link states its reason, making the graph falsifiable
- [[Navigation Over Retrieval]] — the argument that authored structure beats embeddings
- [[Self-Evolving Wiki]] — plain markdown an agent maintains, cross-links, and lints

## Entities

- [[Andrej Karpathy]] — popularized the setup this vault implements
- [[Claude Code]] — the agent that runs the loops
- [[Obsidian]] — the viewer; deliberately not a dependency

## Sources

- [[Karpathy Wiki Setup]] — the description this vault was bootstrapped from

## Open questions

- [[How Should Contradictions Be Resolved]] — the deferral policy is not a resolution policy

## Conventions

Types are `concept`, `entity`, `source`, `moc`, `question`. Status runs
`seed` → `growing` → `evergreen`. Filenames are globally unique so `[[Note Name]]`
resolves from anywhere. The full schema is in `CLAUDE.md`; `scripts/brain_lint.py`
enforces the parts that are machine-checkable.
