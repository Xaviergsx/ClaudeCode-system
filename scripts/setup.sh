#!/usr/bin/env bash
# Install this brain as an Obsidian vault on your machine.
#
#   ./scripts/setup.sh                 # set up in place
#   ./scripts/setup.sh ~/Brain         # copy the scaffold to ~/Brain and set up there
#
# Idempotent: safe to re-run. Never overwrites notes you have written.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-$SRC}"

say()  { printf '  %s\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$*"; }

printf '\n\033[1mbrain setup\033[0m\n\n'

# --- copy scaffold if installing elsewhere ---------------------------------
if [ "$DEST" != "$SRC" ]; then
  say "installing to $DEST"
  mkdir -p "$DEST"
  for item in CLAUDE.md index.md log.md raw wiki templates scripts .claude .obsidian; do
    if [ -e "$DEST/$item" ]; then
      warn "$item already exists — left untouched"
    else
      cp -R "$SRC/$item" "$DEST/$item"
      ok "copied $item"
    fi
  done
  cd "$DEST"
else
  cd "$SRC"
  say "setting up in place: $SRC"
fi

# --- required directories --------------------------------------------------
for dir in raw wiki/concepts wiki/entities wiki/sources wiki/mocs wiki/questions \
           templates scripts .claude/commands .claude/agents .obsidian; do
  mkdir -p "$dir"
done
ok "directory layout"

# --- required files --------------------------------------------------------
missing=0
for file in CLAUDE.md index.md log.md scripts/brain_lint.py; do
  if [ ! -f "$file" ]; then warn "missing: $file"; missing=1; fi
done
[ "$missing" -eq 0 ] && ok "core files present"

chmod +x scripts/brain_lint.py 2>/dev/null || true

# --- python ----------------------------------------------------------------
if command -v python3 >/dev/null 2>&1; then
  ok "python3 $(python3 -c 'import sys;print("%d.%d"%sys.version_info[:2])') — linter will run"
else
  warn "python3 not found; scripts/brain_lint.py will not run (nothing else depends on it)"
fi

# --- claude code -----------------------------------------------------------
if command -v claude >/dev/null 2>&1; then
  ok "claude code found: $(command -v claude)"
else
  warn "claude code not installed — see https://claude.com/claude-code"
fi

# --- obsidian --------------------------------------------------------------
if [ -f .obsidian/app.json ]; then
  ok "obsidian vault config present (open this folder as a vault)"
fi

# --- git -------------------------------------------------------------------
if [ -d .git ]; then
  ok "git repository — your brain is versioned"
elif command -v git >/dev/null 2>&1; then
  say "no git repository here; 'git init' is recommended so revisions are recoverable"
fi

# --- verify ----------------------------------------------------------------
printf '\n'
if command -v python3 >/dev/null 2>&1 && [ -f scripts/brain_lint.py ]; then
  python3 scripts/brain_lint.py --no-color || true
fi

cat <<'NEXT'
  next steps

    1. Open this folder as a vault in Obsidian (Open folder as vault).
    2. Drop something into raw/ — an article, a transcript, a half-formed thought.
    3. Run `claude` in this directory, then `/ingest`.
    4. Later: `/ask <question>`, `/digest`, `/tend`.

NEXT
