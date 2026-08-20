---
description: Ingest raw material into the wiki — read, extract, link, index, log
argument-hint: "[file or 'all'] (default: everything uningested)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3 scripts/brain_lint.py:*)
---

Run the ingestion loop defined in section 5 of `CLAUDE.md`. Target: **$ARGUMENTS**
(if empty, ingest every uningested raw file, oldest first, one at a time).

Start by running `python3 scripts/brain_lint.py --only uningested --no-color` to get the
worklist, and read `index.md` so you know what already exists before creating anything.

For each raw file, in order:

1. **Read it end to end.** Not the first page. If it is long, read it in chunks until you
   reach the end. Do not begin writing until you have.
2. **Write the source note** in `wiki/sources/` from `templates/source.md` — summary,
   claims worth keeping, links out. Set `sources: [raw/<the file>]`.
3. **Extract concepts and entities.** For each, grep `index.md` first. Link if it exists;
   create a `status: seed` stub from the matching template if it does not. Prefer linking.
   If you are about to create more than about eight notes from one document, stop and
   reconsider — you are probably extracting nouns rather than ideas.
4. **Enrich what already exists.** This is the step that creates value: where the new
   material sharpens, extends, or contradicts an existing note, edit that note surgically
   and append the raw path to its `sources`. Contradictions get a `> [!open]` block and a
   question note — never a silent overwrite.
5. **Update `index.md`** with every new note, one line each, description included.
6. **Run `python3 scripts/brain_lint.py --no-color`** and fix what it reports.
7. **Append to `log.md`** — the entry format is in the file. Include what you left undone.
8. **Append the file to the `Ingested` list** in `raw/README.md`. Do not edit the raw file.

Finish the current file completely before starting the next. Report in five lines or
fewer: files ingested, notes created, notes enriched, lint status, questions raised.
