#!/usr/bin/env python3
"""Structural linter for the brain.

Checks the invariants that CLAUDE.md declares: frontmatter schema, unique
filenames, resolvable wikilinks, index coverage, source provenance, atomicity.

Dependency-free by design — the vault should lint on any machine with a
Python 3.9+ interpreter and nothing else.

    python3 scripts/brain_lint.py            # report, exit 1 on errors
    python3 scripts/brain_lint.py --strict   # warnings are errors too
    python3 scripts/brain_lint.py --json     # machine-readable
    python3 scripts/brain_lint.py --only broken-links,orphan
    python3 scripts/brain_lint.py --stats    # just the numbers
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
WIKI = VAULT / "wiki"
RAW = VAULT / "raw"
INDEX = VAULT / "index.md"
LOG = VAULT / "log.md"

VALID_TYPES = {"concept", "entity", "source", "moc", "question"}
VALID_STATUS = {"seed", "growing", "evergreen"}
REQUIRED_KEYS = ("title", "type", "tags", "status", "created", "updated")
# Types that make factual claims and therefore owe an audit trail.
NEEDS_SOURCES = {"concept", "entity", "source"}

MAX_LINES = 400
SEED_MAX_LINES = 40
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TAG_RE = re.compile(r"^[a-z0-9]+(?:[/-][a-z0-9]+)*$")
WIKILINK_RE = re.compile(r"\[\[([^\]\[|#]+)(?:#[^\]\[|]*)?(?:\|([^\]\[]*))?\]\]")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")

SEVERITIES = ("error", "warn", "info")


# ---------------------------------------------------------------- data model


@dataclass
class Finding:
    check: str
    severity: str
    path: str
    line: int
    message: str

    def as_dict(self) -> dict:
        return {
            "check": self.check,
            "severity": self.severity,
            "path": self.path,
            "line": self.line,
            "message": self.message,
        }


@dataclass
class Note:
    path: Path
    rel: str
    stem: str
    lines: list[str]
    meta: dict
    meta_errors: list[str]
    body_start: int
    links: list[tuple[str, int]] = field(default_factory=list)
    inbound: set[str] = field(default_factory=set)

    @property
    def type(self) -> str:
        value = self.meta.get("type")
        return value if isinstance(value, str) else ""

    @property
    def status(self) -> str:
        value = self.meta.get("status")
        return value if isinstance(value, str) else ""


# ------------------------------------------------------------ frontmatter


def parse_frontmatter(lines: list[str]) -> tuple[dict, list[str], int]:
    """Parse a minimal YAML subset: scalars, inline lists, block lists.

    Returns (mapping, errors, index of first body line).
    """
    if not lines or lines[0].strip() != "---":
        return {}, ["missing frontmatter block (file must open with `---`)"], 0

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, ["frontmatter block is never closed"], 0

    meta: dict = {}
    errors: list[str] = []
    key = None

    for raw_line in lines[1:end]:
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        # Continuation of a block list: "  - value"
        if line.startswith((" ", "\t")) and line.lstrip().startswith("- "):
            if key is None:
                errors.append(f"list item with no key: {line.strip()!r}")
                continue
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                meta[key] = []
            meta[key].append(_scalar(line.lstrip()[2:].strip()))
            continue

        if ":" not in line:
            errors.append(f"unparseable frontmatter line: {line.strip()!r}")
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not key:
            errors.append(f"empty key in line: {line.strip()!r}")
            continue
        if key in meta:
            errors.append(f"duplicate key {key!r}")
        meta[key] = _value(value)

    return meta, errors, end + 1


def _value(value: str):
    if value == "":
        return []  # bare key introduces a block list (or an empty field)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part.strip()) for part in inner.split(",") if part.strip()]
    return _scalar(value)


def _scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


# ------------------------------------------------------------------ loading


def strip_code_fences(lines: list[str], start: int = 0) -> list[tuple[str, int]]:
    """Yield (line, 1-based line number) for lines outside fenced code blocks."""
    out: list[tuple[str, int]] = []
    in_fence = False
    for offset, line in enumerate(lines[start:], start=start):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append((line, offset + 1))
    return out


def extract_links(lines: list[str], start: int = 0) -> list[tuple[str, int]]:
    links: list[tuple[str, int]] = []
    for line, number in strip_code_fences(lines, start):
        # Skip inline code so `[[literal]]` in prose about syntax doesn't count.
        cleaned = re.sub(r"`[^`]*`", "", line)
        for match in WIKILINK_RE.finditer(cleaned):
            target = match.group(1).strip()
            if target:
                links.append((target, number))
    return links


def load_notes() -> list[Note]:
    notes: list[Note] = []
    if not WIKI.is_dir():
        return notes
    for path in sorted(WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        meta, meta_errors, body_start = parse_frontmatter(lines)
        note = Note(
            path=path,
            rel=str(path.relative_to(VAULT)),
            stem=path.stem,
            lines=lines,
            meta=meta,
            meta_errors=meta_errors,
            body_start=body_start,
        )
        note.links = extract_links(lines, body_start)
        notes.append(note)
    return notes


# ------------------------------------------------------------------- checks


class Linter:
    def __init__(self, notes: list[Note]) -> None:
        self.notes = notes
        self.findings: list[Finding] = []
        self.by_stem: dict[str, list[Note]] = defaultdict(list)
        self.by_stem_lower: dict[str, list[Note]] = defaultdict(list)
        for note in notes:
            self.by_stem[note.stem].append(note)
            self.by_stem_lower[note.stem.lower()].append(note)

    def add(self, check: str, severity: str, path, line: int, message: str) -> None:
        rel = str(path.relative_to(VAULT)) if isinstance(path, Path) else str(path)
        self.findings.append(Finding(check, severity, rel, line, message))

    # -- schema ---------------------------------------------------------

    def check_frontmatter(self) -> None:
        today = date.today().isoformat()
        for note in self.notes:
            for error in note.meta_errors:
                self.add("frontmatter", "error", note.path, 1, error)
            if not note.meta:
                continue

            for key in REQUIRED_KEYS:
                if key not in note.meta:
                    self.add("frontmatter", "error", note.path, 1,
                             f"missing required key `{key}`")

            title = note.meta.get("title")
            if isinstance(title, str) and title and title != note.stem:
                self.add("title-mismatch", "error", note.path, 1,
                         f"title {title!r} does not match filename {note.stem!r}")

            note_type = note.meta.get("type")
            if isinstance(note_type, str) and note_type and note_type not in VALID_TYPES:
                self.add("frontmatter", "error", note.path, 1,
                         f"type {note_type!r} not in {sorted(VALID_TYPES)}")

            status = note.meta.get("status")
            if isinstance(status, str) and status and status not in VALID_STATUS:
                self.add("frontmatter", "error", note.path, 1,
                         f"status {status!r} not in {sorted(VALID_STATUS)}")

            tags = note.meta.get("tags")
            if not isinstance(tags, list):
                if "tags" in note.meta:
                    self.add("frontmatter", "error", note.path, 1,
                             "tags must be a list, e.g. [ai/rag, tooling]")
            elif not tags:
                self.add("frontmatter", "warn", note.path, 1, "no tags")
            else:
                for tag in tags:
                    if not TAG_RE.match(str(tag)):
                        self.add("tag-format", "warn", note.path, 1,
                                 f"tag {tag!r} is not lowercase/slash-separated")

            for key in ("created", "updated"):
                value = note.meta.get(key)
                if isinstance(value, str) and value and not DATE_RE.match(value):
                    self.add("frontmatter", "error", note.path, 1,
                             f"{key} {value!r} is not YYYY-MM-DD")
                elif isinstance(value, str) and DATE_RE.match(value or "") and value > today:
                    self.add("frontmatter", "warn", note.path, 1,
                             f"{key} {value} is in the future")

            created, updated = note.meta.get("created"), note.meta.get("updated")
            if (isinstance(created, str) and isinstance(updated, str)
                    and DATE_RE.match(created or "") and DATE_RE.match(updated or "")
                    and updated < created):
                self.add("frontmatter", "error", note.path, 1,
                         f"updated {updated} precedes created {created}")

    def check_unique_filenames(self) -> None:
        for stem, notes in sorted(self.by_stem.items()):
            if len(notes) > 1:
                others = ", ".join(n.rel for n in notes[1:])
                self.add("duplicate-name", "error", notes[0].path, 1,
                         f"filename {stem!r} is not unique; also at {others}")
        for lower, notes in sorted(self.by_stem_lower.items()):
            distinct = {n.stem for n in notes}
            if len(distinct) > 1:
                self.add("duplicate-name", "warn", notes[0].path, 1,
                         f"names differ only by case: {sorted(distinct)}")

    # -- links ----------------------------------------------------------

    def resolve(self, target: str) -> Note | None:
        if target in self.by_stem:
            return self.by_stem[target][0]
        candidates = self.by_stem_lower.get(target.lower())
        return candidates[0] if candidates else None

    def check_links(self) -> None:
        for note in self.notes:
            for target, line in note.links:
                # Path-style links (raw/foo.md) resolve against the vault root.
                if "/" in target or target.endswith(".md"):
                    candidate = VAULT / target
                    if not candidate.exists() and not candidate.with_suffix(".md").exists():
                        self.add("broken-link", "error", note.path, line,
                                 f"[[{target}]] does not resolve to a file")
                    continue

                resolved = self.resolve(target)
                if resolved is None:
                    self.add("broken-link", "error", note.path, line,
                             f"[[{target}]] has no matching note in wiki/")
                    continue
                if resolved.stem != target:
                    self.add("link-case", "warn", note.path, line,
                             f"[[{target}]] resolves to {resolved.stem!r} by case-folding")
                if resolved.rel == note.rel:
                    self.add("self-link", "warn", note.path, line,
                             "note links to itself")
                else:
                    resolved.inbound.add(note.stem)

    def check_orphans(self) -> None:
        for note in self.notes:
            if note.type == "moc":
                continue  # hubs are entry points; nothing needs to link them
            if note.inbound:
                continue
            if self._linked_from_index(note):
                self.add("orphan", "info", note.path, 1,
                         "reachable only from index.md — consider linking it from a note")
            else:
                self.add("orphan", "warn", note.path, 1,
                         "no inbound links from any note or index.md")

    def _linked_from_index(self, note: Note) -> bool:
        return note.stem in self.index_targets

    def check_dead_ends(self) -> None:
        for note in self.notes:
            if note.type == "question":
                continue
            outbound = {t for t, _ in note.links}
            if outbound:
                continue
            severity = "info" if note.status == "seed" else "warn"
            self.add("dead-end", severity, note.path, 1,
                     "no outbound links — every note needs a Connections section")

    def check_bare_links(self) -> None:
        """Inside `## Connections`, every link line must explain itself."""
        for note in self.notes:
            in_section = False
            for line, number in strip_code_fences(note.lines, note.body_start):
                stripped = line.strip()
                if stripped.startswith("#"):
                    in_section = stripped.lower().lstrip("# ").startswith("connections")
                    continue
                if not in_section or not stripped.startswith(("-", "*")):
                    continue
                if not WIKILINK_RE.search(stripped):
                    continue
                remainder = WIKILINK_RE.sub("", stripped).strip(" -*\t")
                if len(remainder) < 8:
                    self.add("bare-link", "warn", note.path, number,
                             "connection has no reason attached (use `— why it relates`)")

    # -- provenance -----------------------------------------------------

    def check_sources(self) -> None:
        for note in self.notes:
            if not note.meta:
                continue
            sources = note.meta.get("sources", [])
            if isinstance(sources, str):
                sources = [sources] if sources else []
            if not isinstance(sources, list):
                self.add("sources", "error", note.path, 1, "sources must be a list")
                continue

            if note.type in NEEDS_SOURCES and not sources:
                severity = "info" if note.status == "seed" else "warn"
                self.add("sources", severity, note.path, 1,
                         f"type `{note.type}` has no entry in `sources`")

            for source in sources:
                source = str(source).strip().strip("[]")
                if not source:
                    continue
                if not (VAULT / source).exists():
                    self.add("sources", "error", note.path, 1,
                             f"source {source!r} does not exist")
                elif not source.startswith("raw/"):
                    self.add("sources", "warn", note.path, 1,
                             f"source {source!r} should be a path into raw/")

    def check_raw_ingestion(self) -> None:
        if not RAW.is_dir():
            return
        cited: set[str] = set()
        for note in self.notes:
            sources = note.meta.get("sources", [])
            if isinstance(sources, str):
                sources = [sources]
            if isinstance(sources, list):
                for source in sources:
                    cited.add(str(source).strip().strip("[]"))

        readme = RAW / "README.md"
        declared = readme.read_text(encoding="utf-8") if readme.exists() else ""

        for path in sorted(RAW.rglob("*")):
            if path.is_dir() or path.name.startswith("."):
                continue
            rel = str(path.relative_to(VAULT))
            if path.name == "README.md":
                continue
            if rel in cited:
                continue
            if rel in declared:
                self.add("uningested", "info", path, 1,
                         "listed as ingested but no wiki note cites it in `sources`")
            else:
                self.add("uningested", "warn", path, 1,
                         "raw file has never been ingested (run /ingest)")

    # -- shape ----------------------------------------------------------

    def check_size(self) -> None:
        for note in self.notes:
            count = len(note.lines)
            if count > MAX_LINES:
                self.add("too-long", "warn", note.path, 1,
                         f"{count} lines exceeds {MAX_LINES}; split it and leave a hub")
            if note.status == "seed" and count > SEED_MAX_LINES:
                self.add("stale-status", "info", note.path, 1,
                         f"{count} lines but still `status: seed` — promote to `growing`")

    def check_headings(self) -> None:
        for note in self.notes:
            body = [ln for ln, _ in strip_code_fences(note.lines, note.body_start)]
            h1s = [ln for ln in body if ln.startswith("# ")]
            if not h1s:
                self.add("headings", "warn", note.path, note.body_start + 1,
                         "no H1 heading in body")
            elif len(h1s) > 1:
                self.add("headings", "warn", note.path, note.body_start + 1,
                         f"{len(h1s)} H1 headings — one note, one title")
            elif isinstance(note.meta.get("title"), str):
                heading = h1s[0][2:].strip()
                if heading != note.meta["title"]:
                    self.add("headings", "warn", note.path, note.body_start + 1,
                             f"H1 {heading!r} differs from title {note.meta['title']!r}")

    def check_tag_singletons(self) -> None:
        counts: dict[str, list[Note]] = defaultdict(list)
        for note in self.notes:
            tags = note.meta.get("tags")
            if isinstance(tags, list):
                for tag in tags:
                    counts[str(tag)].append(note)
        for tag, notes in sorted(counts.items()):
            if len(notes) == 1:
                self.add("singleton-tag", "info", notes[0].path, 1,
                         f"tag {tag!r} is used by exactly one note")

    # -- index and log ---------------------------------------------------

    def load_index(self) -> None:
        self.index_targets: set[str] = set()
        if not INDEX.exists():
            self.add("index", "error", INDEX, 1, "index.md is missing")
            return
        lines = INDEX.read_text(encoding="utf-8").splitlines()
        for target, line in extract_links(lines):
            if "/" in target:
                continue
            self.index_targets.add(target)
            if self.resolve(target) is None:
                self.add("index", "error", INDEX, line,
                         f"index lists [[{target}]] but no such note exists")

    def check_index_coverage(self) -> None:
        if not INDEX.exists():
            return
        for note in self.notes:
            if note.stem not in self.index_targets:
                self.add("index", "warn", note.path, 1,
                         "note is not listed in index.md")

    def check_log(self) -> None:
        if not LOG.exists():
            self.add("log", "error", LOG, 1, "log.md is missing")
            return
        text = LOG.read_text(encoding="utf-8")
        if not re.search(r"\d{4}-\d{2}-\d{2}", text):
            self.add("log", "warn", LOG, 1, "log.md contains no dated entries")

    # -- driver ----------------------------------------------------------

    def run(self) -> list[Finding]:
        self.check_frontmatter()
        self.check_unique_filenames()
        self.check_links()          # populates inbound
        self.load_index()           # populates index_targets
        self.check_orphans()        # needs both
        self.check_index_coverage()
        self.check_dead_ends()
        self.check_bare_links()
        self.check_sources()
        self.check_raw_ingestion()
        self.check_size()
        self.check_headings()
        self.check_tag_singletons()
        self.check_log()
        return self.findings


# ------------------------------------------------------------------ output


def build_stats(notes: list[Note]) -> dict:
    by_type: dict[str, int] = defaultdict(int)
    by_status: dict[str, int] = defaultdict(int)
    tags: set[str] = set()
    links = 0
    for note in notes:
        by_type[note.type or "?"] += 1
        by_status[note.status or "?"] += 1
        links += len(note.links)
        if isinstance(note.meta.get("tags"), list):
            tags.update(str(t) for t in note.meta["tags"])
    raw_count = 0
    if RAW.is_dir():
        raw_count = sum(
            1 for p in RAW.rglob("*")
            if p.is_file() and p.name != "README.md" and not p.name.startswith(".")
        )
    return {
        "notes": len(notes),
        "links": links,
        "links_per_note": round(links / len(notes), 2) if notes else 0.0,
        "raw_files": raw_count,
        "tags": len(tags),
        "by_type": dict(sorted(by_type.items())),
        "by_status": dict(sorted(by_status.items())),
    }


def colorize(text: str, code: str, enabled: bool) -> str:
    return f"\033[{code}m{text}\033[0m" if enabled else text


def render(findings: list[Finding], stats: dict, color: bool) -> str:
    out: list[str] = []
    palette = {"error": "31", "warn": "33", "info": "36"}

    out.append(colorize("brain lint", "1", color))
    out.append(
        f"  {stats['notes']} notes · {stats['links']} links "
        f"({stats['links_per_note']}/note) · {stats['raw_files']} raw · "
        f"{stats['tags']} tags"
    )
    if stats["by_status"]:
        parts = ", ".join(f"{k} {v}" for k, v in stats["by_status"].items())
        out.append(f"  status: {parts}")
    if stats["by_type"]:
        parts = ", ".join(f"{k} {v}" for k, v in stats["by_type"].items())
        out.append(f"  type:   {parts}")
    out.append("")

    if not findings:
        out.append(colorize("  clean — no findings", "32", color))
        out.append("")
        return "\n".join(out)

    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.check].append(finding)

    for check in sorted(grouped, key=lambda c: (
        SEVERITIES.index(min((f.severity for f in grouped[c]), key=SEVERITIES.index)), c
    )):
        items = grouped[check]
        worst = min((f.severity for f in items), key=SEVERITIES.index)
        header = colorize(f"{check} ({len(items)})", palette[worst], color)
        out.append(f"  {header}")
        for finding in items:
            location = f"{finding.path}:{finding.line}"
            out.append(f"    {location:<44} {finding.message}")
        out.append("")

    counts = {s: sum(1 for f in findings if f.severity == s) for s in SEVERITIES}
    summary = ", ".join(f"{counts[s]} {s}" for s in SEVERITIES if counts[s])
    out.append(f"  {summary}")
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint the markdown brain.")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    parser.add_argument("--stats", action="store_true", help="print stats only")
    parser.add_argument("--only", default="", help="comma-separated check names")
    parser.add_argument("--severity", default="info", choices=SEVERITIES,
                        help="minimum severity to report (default: info)")
    parser.add_argument("--no-color", action="store_true")
    args = parser.parse_args(argv)

    notes = load_notes()
    stats = build_stats(notes)

    if args.stats:
        print(json.dumps(stats, indent=2) if args.json
              else render([], stats, not args.no_color))
        return 0

    findings = Linter(notes).run()

    if args.only:
        wanted = {name.strip() for name in args.only.split(",") if name.strip()}
        findings = [f for f in findings if f.check in wanted]

    threshold = SEVERITIES.index(args.severity)
    findings = [f for f in findings if SEVERITIES.index(f.severity) <= threshold]
    findings.sort(key=lambda f: (SEVERITIES.index(f.severity), f.check, f.path, f.line))

    color = not args.no_color and sys.stdout.isatty() and os.environ.get("TERM") != "dumb"

    if args.json:
        print(json.dumps(
            {"stats": stats, "findings": [f.as_dict() for f in findings]}, indent=2
        ))
    else:
        print(render(findings, stats, color))

    failing = {"error", "warn"} if args.strict else {"error"}
    return 1 if any(f.severity in failing for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
