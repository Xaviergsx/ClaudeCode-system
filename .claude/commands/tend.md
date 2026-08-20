---
description: Maintenance pass — lint, fix, merge, split, promote, strengthen links
argument-hint: "[area or note name] (default: whole vault)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3 scripts/brain_lint.py:*)
---

Run the maintenance loop from section 6 of `CLAUDE.md`. Scope: **$ARGUMENTS**
(if empty, the whole vault).

This pass makes the brain *better*, not bigger. Creating new notes is mostly out of scope.

1. **Lint first.** `python3 scripts/brain_lint.py --no-color`. Fix every error. Fix the
   warnings that are real; for any you leave, say why in `log.md`.
2. **Orphans and dead ends.** A note nothing links to is either mis-filed or was never
   worth writing. Connect it from the right place, or merge it away.
3. **Missing edges.** Find pairs of notes that should link and don't — the highest-value
   work in this pass. Add the link on **both** sides, each with its reason.
4. **Promote.** `seed` notes that now carry real content become `growing`. `growing` notes
   that read well standalone and have settled become `evergreen`.
5. **Split and merge.** Split notes covering two ideas, leaving a hub. Merge near-duplicates
   into the better-named one, leaving a redirect stub.
6. **Rewrite one note.** Pick the worst-written `evergreen` note and fix its prose. One,
   not ten.
7. **Reconcile `index.md`**, then append to `log.md`.

Hard limits: no mass reformatting — if you find yourself making the same edit across more
than about ten files, stop and ask first. Never delete a note; merge or redirect. Never
touch `raw/`.

Report what you changed and, specifically, what you chose not to change and why.
