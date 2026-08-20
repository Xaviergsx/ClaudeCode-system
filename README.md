# Claude Brain

A self-evolving markdown wiki that Claude Code maintains for you, viewable in Obsidian.

Plain text instead of a vector database. You drop raw material into `raw/`; Claude reads
it, writes interlinked atomic notes into `wiki/`, keeps `index.md` and `log.md` current,
and lints its own work. Over time it doesn't just accumulate — it merges duplicates,
splits overgrown notes, promotes matured ones, and connects things you didn't notice were
related.

The vault ships seeded with 13 notes about its own method, so the graph is populated and
the conventions are demonstrated rather than described.

## Install

```bash
git clone <this repo> ~/Brain && cd ~/Brain
./scripts/setup.sh
```

Or install the scaffold somewhere else, leaving this repo alone:

```bash
./scripts/setup.sh ~/Documents/MyVault
```

Then:

1. **Obsidian** → *Open folder as vault* → pick the directory. Config, graph colors, and
   hotkeys are already set up.
2. `cd` into it and run `claude`.
3. `/ingest`.

Requires Claude Code. Python 3.9+ is needed only for the linter; nothing else depends on
it. Obsidian is optional — it is a viewer, and the vault is just text files.

## Layout

```
CLAUDE.md      the charter — rules the agent obeys every session
index.md       flat map of every note, one line each
log.md         append-only journal of what changed and why
raw/           inbox. Immutable source material.
wiki/          the brain: concepts, entities, sources, mocs, questions
templates/     frontmatter skeletons
scripts/       brain_lint.py — the structural check
.claude/       commands and subagents
```

## Commands

| Command | What it does |
|---|---|
| `/capture <thought>` | Writes straight to `raw/`. No structuring — capture must cost nothing. |
| `/ingest [file]` | The core loop: read raw → source note → extract concepts → enrich existing notes → index → log. |
| `/ask <question>` | Answers from the vault, citing notes, flagging what's missing. Read-only. |
| `/tend [area]` | Maintenance: fix lint, connect orphans, merge duplicates, promote notes. |
| `/digest [since]` | State of the brain: growth, health, thin spots, what to do next. |

Two subagents in `.claude/agents/` — `librarian` (ingests one document with a clean
context) and `gardener` (maintenance only) — for when you want the work isolated from
your main session.

## The linter

```bash
python3 scripts/brain_lint.py           # report; exit 1 on errors
python3 scripts/brain_lint.py --strict  # warnings fail too
python3 scripts/brain_lint.py --json    # machine-readable
python3 scripts/brain_lint.py --stats   # just the numbers
```

Thirteen checks, dependency-free: frontmatter schema, filename uniqueness, broken
wikilinks, orphans, dead ends, unexplained links, index coverage, source provenance,
uningested raw files, note size, heading consistency, tag hygiene, log presence.

Findings are `error` (breaks an invariant), `warn` (real problem, needs judgment), or
`info` (worth knowing). The agent runs this at the end of every writing session and fixes
what it reports.

## How it actually works

Three ideas carry the design:

**Capture and structure are separate.** Capture is cheap and constant; structure is
deliberate and scheduled. `/capture` never organizes anything and `/ingest` never
invents anything. Conflating them is what makes most note systems collapse.

**Every claim traces to a source.** Notes carry a `sources:` list pointing into `raw/`.
Because raw files are immutable, provenance survives every later reorganization, and the
linter can tell you which notes are asserting things with no backing.

**Links carry their reason.** `[[Transformers]] — RAG retrofits memory onto them` rather
than a bare link. This makes the graph readable as prose, lets an agent learn a
neighbourhood from one section instead of five files, and makes bad structure findable —
a stated reason can be wrong, a bare link never can.

The governance lives in `CLAUDE.md`: think first, edit surgically, never invent facts,
never delete knowledge, always log. It's read at the start of every session, so the rules
survive new machines and new sessions rather than living in your prompting habits.

## Changing the rules

`CLAUDE.md` is the schema; editing it changes the agent's behavior everywhere. The
permissions in `.claude/settings.json` deliberately deny the agent write access to
`CLAUDE.md`, `scripts/`, and `templates/` — those are yours to change, on purpose, in a
conversation about the rules rather than as a side effect of filing a document.
