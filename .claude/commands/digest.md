---
description: Report on the state of the brain — growth, gaps, and what to do next
argument-hint: "[since YYYY-MM-DD]"
allowed-tools: Read, Glob, Grep, Bash(python3 scripts/brain_lint.py:*), Bash(git log:*), Bash(git diff:*)
---

Report on the state of the brain. Window: **$ARGUMENTS** (default: since the last `log.md`
entry). Read-only — produce a report, change nothing.

Gather:

- `python3 scripts/brain_lint.py --stats --no-color` for the shape of the vault.
- `python3 scripts/brain_lint.py --json --no-color` for the findings.
- `log.md` for what recent sessions claim to have done.
- `git log --oneline` over the window, if this is a git repository.

Then report, in this order and briefly:

1. **Growth** — notes and links added, what subject areas grew.
2. **Health** — lint findings by severity. Orphan and dead-end counts are the real signal:
   rising orphans mean ingestion is outrunning curation.
3. **Thin spots** — `seed` notes with many inbound links. These are the highest-value
   things to write next, because the vault keeps pointing at them and they say nothing.
4. **Unresolved** — every `> [!open]` block and question note, oldest first. Call out any
   that has been open a long time.
5. **Backlog** — uningested raw files.
6. **Do next** — three specific recommendations, most valuable first. Name the notes.
   "Run /tend" is not a recommendation; "merge [[X]] into [[Y]], they say the same thing"
   is.
