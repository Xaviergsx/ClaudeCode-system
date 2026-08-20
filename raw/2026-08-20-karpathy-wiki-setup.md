# Raw capture — the Karpathy-style Claude + markdown brain

Captured 2026-08-20. Source: user-provided description of Andrej Karpathy's setup.

---

Andrej Karpathy's viral setup combines Claude Code with a local markdown folder (often
viewed via Obsidian) to create a "Self-Evolving LLM Wiki" — an optimized,
behavior-governed workflow. It replaces complex vector databases with plain text files
that Claude maintains, cross-links, and "lints" autonomously over time.

## Core components of the setup

- **The raw folder (`raw/`)** — drops raw incoming data like PDFs, notes, or YouTube
  transcripts.
- **The wiki folder (`wiki/`)** — interlinked markdown pages where Claude organizes
  concepts, entities, and summaries.
- **The schema / configuration (`CLAUDE.md`)** — root instructions dictating agent
  boundaries, behavioral guardrails, and structural rules.
- **The index and log (`index.md`, `log.md`)** — high-level maps for Claude to navigate
  its own long-term memory and track operations.

## Step-by-step implementation

1. **Create directory.** Make a clean local directory (e.g. your Obsidian vault) with
   subfolders for `raw/` and `wiki/`.
2. **Add `CLAUDE.md`.** Drop in a configuration file outlining strict execution
   constraints — Karpathy's rules on thinking first, surgical edits, and avoiding
   over-engineering.
3. **Point Claude Code at it.** Open a terminal inside the folder and run `claude`.
4. **Initialize ingestion.** Prompt Claude Code to read the raw files, structure them
   into interconnected markdown nodes, update the index, and maintain the wiki
   iteratively.

## Notes on why it works

The claim is that plain text plus an agent that can grep, read, and rewrite beats a
vector database for personal knowledge, because the retrieval step is *navigation over a
structure the agent itself built* rather than nearest-neighbour lookup over opaque
embeddings. The structure is legible, diffable, and portable. Obsidian is only a viewer;
nothing depends on it.
