# raw/ — the inbox

Drop source material here and it becomes fair game for ingestion. Anything goes:
exported PDFs, article clippings, YouTube transcripts, meeting notes, voice-memo
transcriptions, half-finished thoughts.

## Rules

- **These files are immutable.** Claude reads them and never rewrites them. The one
  exception is the `Ingested` list at the bottom of this file.
- **Name files `YYYY-MM-DD-short-slug.ext`** when you can. The date is the capture date,
  not the publication date — put the publication date in the note that comes out of it.
- **One document per file.** Two articles in one file produce a muddled source note.
- **Messy is fine.** Formatting doesn't matter. Half-sentences are fine. The point of
  this folder is that capture should cost nothing.

## What happens to them

`/ingest` reads a raw file end to end, writes one source note under `wiki/sources/`,
extracts the concepts and entities worth their own pages, enriches whatever already
exists, and updates `index.md` and `log.md`. The raw file stays exactly as you left it —
it is the audit trail that every claim in the wiki traces back to.

Anything sitting here that no wiki note cites in its `sources` frontmatter is reported by
`brain_lint.py` as `uningested`. That report is your worklist.

## Ingested

Files that have been through the loop. Append as you go — path, date, resulting note.

- `raw/2026-08-20-karpathy-wiki-setup.md` — 2026-08-20 → [[Karpathy Wiki Setup]]
