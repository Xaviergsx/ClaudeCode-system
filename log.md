# Log

Append-only record of every session that wrote to this vault. Newest first. One entry per
session: what came in, what was created, what changed, what was deliberately left undone.

The log exists so that a future session — or a future you — can reconstruct why the vault
looks the way it does without reading every diff.

---

## 2026-08-20 — bootstrap

**Ingested:** `raw/2026-08-20-karpathy-wiki-setup.md`

**Created (13 notes):**
- Source: [[Karpathy Wiki Setup]]
- Concepts: [[Self-Evolving Wiki]], [[Agentic Ingestion Loop]], [[Atomic Notes]],
  [[Link As Assertion]], [[Context Engineering]], [[Navigation Over Retrieval]]
- Entities: [[Claude Code]], [[Obsidian]], [[Andrej Karpathy]]
- Maps: [[Home]], [[Knowledge Systems]]
- Question: [[How Should Contradictions Be Resolved]]

**Changed:** `index.md` created and populated. `raw/README.md` ingested-list seeded.

**Structure established:** `CLAUDE.md` charter, note schema, `scripts/brain_lint.py`,
templates, and the `/ingest`, `/tend`, `/ask`, `/capture`, `/digest` commands.

**Left undone, deliberately:**
- The three entity notes are `status: seed`. They caught links from the source document
  and have not been researched independently; growing them needs material that is not in
  `raw/` yet.
- [[Navigation Over Retrieval]] carries an open question about scaling limits that the
  source does not address. Not resolvable from current material.
- No second source has been ingested, so no note has yet been enriched by conflicting
  evidence — the step-4 enrichment path in [[Agentic Ingestion Loop]] is untested against
  real disagreement.
