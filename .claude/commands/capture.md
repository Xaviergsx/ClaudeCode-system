---
description: Write a thought straight into raw/ without breaking flow
argument-hint: "<the thought, or a URL, or a paste>"
allowed-tools: Write, Bash(date:*)
---

Capture this into `raw/` immediately: **$ARGUMENTS**

The entire point is that capture costs nothing. Do exactly this and stop:

1. Write the content verbatim to `raw/YYYY-MM-DD-<short-slug>.md` using today's date and
   a slug drawn from the content. If a file with that name exists, append to it under a
   `---` separator rather than creating a variant.
2. Add a one-line header noting the capture date and, if given, where it came from.
3. Confirm the path in one line.

Do **not** ingest it. Do not create wiki notes, do not update `index.md`, do not lint, do
not tidy the wording. Capture and structure are separate operations on purpose — run
`/ingest` when you want the structure to catch up.
