---
description: Answer a question from the wiki, citing notes, and flag what's missing
argument-hint: "<your question>"
allowed-tools: Read, Glob, Grep
---

Answer this question using the brain: **$ARGUMENTS**

This is a **read-only** command. Do not create, edit, or reorganize anything, however
tempting — if the vault is missing something, say so at the end rather than fixing it.

Method:

1. Read `index.md` to see what exists.
2. Grep for the concepts involved. Follow links outward from what you find — the
   `## Connections` sections are written to be read this way, so use them to navigate
   rather than opening every file.
3. Answer from what the notes actually say. Cite each claim with the note it came from,
   as `[[Note Name]]`.

Rules for the answer:

- **Distinguish sources.** What the vault asserts, versus what you know independently and
  the vault does not contain. Mark the latter explicitly. Never blur them.
- **Report contradictions** between notes rather than picking a winner silently.
- **Say what is missing.** End with the gaps: which notes are thin, which are `seed`, and
  what would need to be captured into `raw/` to answer this properly.

If the vault has nothing relevant, say exactly that in one line. Do not pad the answer
with general knowledge dressed up as vault content.
