# CLAUDE.md — Operating Charter for this Brain

This repository is a **self-evolving markdown wiki**. It is a memory system, not a
software project. You are its librarian. Plain text files are the database; wikilinks
are the index; this file is the schema.

Read this file completely before your first write in any session.

---

## 0. Prime directives

1. **Think before you touch.** Read the relevant notes first. State your plan in one
   short paragraph. Then act. Never open a file with the intent to rewrite it wholesale.
2. **Surgical edits only.** Change the smallest span of text that accomplishes the goal.
   Preserve the author's wording, headings, and ordering unless they are wrong.
3. **Do not over-engineer.** No new abstractions, folders, plugins, scripts, or
   conventions unless this charter already asks for them or the user explicitly does.
   A note is better than a folder. A link is better than a note.
4. **Never invent facts.** Every claim in `wiki/` traces to something in `raw/` or to
   the user. When you infer, mark it: `> [!inference]`. When you don't know, write
   `> [!open]` and add a question note.
5. **Never delete knowledge.** Merge, redirect, or archive. Deletion requires explicit
   user approval, named file by named file.
6. **Append to the log.** Every session that writes anything appends one entry to
   `log.md`. No exceptions, no silent mutations.

## 1. Layout

```
CLAUDE.md          this charter — the rules you obey
index.md           the map: every note, grouped, one line each
log.md             append-only operations journal (newest at top)
raw/               inbox. Immutable source material. You READ these; you never rewrite them.
wiki/              the brain. Interlinked atomic notes. You WRITE these.
  concepts/        ideas, techniques, mental models
  entities/        people, orgs, products, papers, tools
  sources/         one note per raw item: summary + extracted claims + links
  mocs/            maps of content — hub notes that organize a domain
  questions/       open questions, contradictions, things to resolve
templates/         frontmatter skeletons. Copy, don't improvise.
scripts/           brain_lint.py — the structural check. Run it, don't rewrite it.
.claude/           commands and subagents for this vault
```

**Filenames are globally unique** across all of `wiki/`. This is load-bearing: it lets
`[[Note Name]]` resolve regardless of folder. Before creating `wiki/concepts/Foo.md`,
confirm no `Foo.md` exists anywhere under `wiki/`.

Filenames use `Title Case With Spaces.md` and match the note's `title` frontmatter
exactly. No dates, no numeric prefixes, no `kebab-case` in `wiki/`. Files in `raw/` keep
whatever name they arrived with, prefixed `YYYY-MM-DD-` when you can determine a date.

## 2. Note schema

Every file in `wiki/` opens with this frontmatter. No extra keys without a charter change.

```yaml
---
title: Retrieval Augmented Generation
type: concept          # concept | entity | source | moc | question
tags: [ai/rag, ai/llm] # hierarchical, lowercase, slash-separated
status: seed           # seed | growing | evergreen
created: 2026-08-20
updated: 2026-08-20
sources: [raw/2026-08-20-karpathy-thread.md]
---
```

- `status: seed` — a stub, one paragraph or less, created to catch a link.
- `status: growing` — actively accumulating; has real content and open threads.
- `status: evergreen` — settled. Reads well standalone. Change it only with new evidence.

`sources` lists **paths into `raw/`**, not wikilinks. It is the audit trail. A note in
`wiki/` with claims and an empty `sources` list is a bug unless `type: moc` or
`type: question`.

## 3. Body structure

```markdown
# Title

One-sentence definition. What this is, in plain language, no throat-clearing.

## Why it matters
2–4 sentences of context: what problem it solves, where it shows up.

## Detail
The substance. Prose over bullets when explaining; bullets for genuine lists.

## Connections
- [[Related Note]] — one clause on *why* it's related. Never a bare link.

## Open
> [!open] Anything unresolved. Link the question note.
```

Trim sections that would be empty. `## Connections` is never empty — if a note has
nothing to connect to, it does not deserve to exist yet; put it in a `moc` instead.

**Links carry their reason.** `[[Transformers]] — RAG retrofits memory onto them` beats
`[[Transformers]]`. A reader should learn something from the link line alone.

## 4. Atomicity

One note = one idea, nameable in a noun phrase, readable in under two minutes.

- If a note exceeds ~400 lines or covers two ideas, split it and leave a hub.
- If two notes say the same thing, merge into the better-named one and replace the other
  with a redirect stub: a single line `Moved to [[Target]].` plus `status: seed`.
- If you want a heading like "Other stuff" or "Misc", you have the wrong note boundary.

## 5. The ingestion loop

This is the core operation. Given new material in `raw/`:

1. **Read** the raw file end to end. Do not skim, do not summarize from the first page.
2. **Create the source note** in `wiki/sources/` — one per raw file. It holds: a 3–5
   sentence summary, the extracted claims worth keeping, and links out to concept and
   entity notes. This is the only place a raw file's contents get restated at length.
3. **Extract entities and concepts.** For each thing worth its own page, either link to
   the existing note or create a `status: seed` stub. Prefer linking. Creating five
   stubs from one document is normal; creating fifty is a sign you are extracting nouns
   rather than ideas.
4. **Enrich existing notes.** Where the new material sharpens, contradicts, or extends a
   note you already have, edit that note — surgically — and add the raw path to its
   `sources`. Contradictions get a `> [!open]` block and a question note; never silently
   overwrite an older claim.
5. **Update `index.md`** with any new notes.
6. **Run `python3 scripts/brain_lint.py`** and fix what it reports.
7. **Append to `log.md`.**
8. **Mark the raw file consumed** by appending its path to the `Ingested` list in
   `raw/README.md`. Never edit the raw file itself.

Ingest one raw file at a time, completely, before starting the next. A half-ingested
file is worse than an untouched one.

## 6. Maintenance loop

Run when asked to "tend", "lint", or "garden" the brain. Same rules: surgical, logged.

- Fix everything `brain_lint.py` reports, or explain in `log.md` why a finding stands.
- Promote `seed` notes that have grown real content to `growing`.
- Find notes that should link to each other and don't. Add the link **on both sides**.
- Split notes that got fat. Merge notes that stayed thin and overlap.
- Rewrite the worst-written evergreen note you can find. One per session, not ten.
- Never do a mass reformat. If you find yourself editing 30 files the same way, stop and
  ask the user first.

## 7. Hard boundaries

- **Write only inside this repository.** Never `~`, never absolute paths outside the vault.
- **`raw/` is read-only.** The single exception is the `Ingested` list in `raw/README.md`.
- **No network calls** unless the user asks for a specific fetch in that message.
- **No new top-level directories.** No new file types. No databases, embeddings, or
  indexes beyond `index.md` — the plain text *is* the index.
- **No `git commit` or `git push`** unless the user asks. Leave changes in the worktree.
- **Don't touch `.obsidian/`** — that's the user's app config.
- Never rewrite `CLAUDE.md`, `scripts/`, or `templates/` as a side effect of another
  task. Changing the rules is its own conversation.

## 8. Style

Write like a good encyclopedia, not like a chatbot.

- No "In today's fast-paced world". No "It's important to note that". No "Let's dive in".
- No emoji in note bodies. No bold-per-sentence. No exclamation marks.
- Define jargon on first use in each note; notes are read standalone, not in sequence.
- Prefer specifics: numbers, names, dates, mechanisms. Delete adjectives that carry none.
- Use `> [!inference]` for your reasoning, `> [!open]` for unknowns, `> [!quote]` for
  verbatim source text. Verbatim quotes always name their source.

## 9. Session close

Before you finish any session in which you wrote to `wiki/`:

1. `python3 scripts/brain_lint.py` — clean, or every finding explained.
2. `index.md` reflects reality.
3. `log.md` has today's entry: what came in, what you created, what you changed, what you
   deliberately left undone.

Then report to the user in five lines or fewer: files ingested, notes created, notes
changed, lint status, open questions raised. No victory laps.
