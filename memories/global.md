# Global memory rules (always loaded)

Memory root: `C:\ai\memories\` (Git Bash: `/c/ai/memories/`), shared by all projects and loaded for every project from `~/.claude/CLAUDE.md`. Keep this file short.

1. **Load on demand.** Don't read every memory file up front. Use `index.md` (files + **Topics** table: `#tag` → entry IDs across all files) and prefer `Grep` on a keyword, `#tag` or ID (`I-001`) over reading a whole file.
2. **On any non-trivial error:** grep `categories/issues.md` (and `limitations.md`) for the error text, tool or `#tag` before retrying. Don't rerun the same command unchanged or stack guesses.
3. **Before a large or long-horizon task:** look up the task's topics in `index.md` → Topics (issues, successes, procedures, references), and read the project's `projects/<name>.md`.
4. **Record only what's noteworthy:** non-obvious failures, hard-won fixes, validated workflows, lasting decisions, stated user preferences, useful commands and docs. Skip typos and routine work.
5. **Every memory change goes through the `memory-optimizer` skill:** check existing entries first; edit if it exists, otherwise add it with the next free ID and its `#tags`; one entry lives in exactly one file. Link entries by ID, never by position.
6. **Central memory only.** Never save memories in Claude Code's per-project auto-memory (`~/.claude/projects/<proj>/memory/`) or project folders; those hold only a pointer here. Reusable scripts go in `C:\ai\toolbox\`, not a session scratchpad.
7. **End of a noteworthy task/session:** run `memory-optimizer`'s end-of-task workflow — Phase A upserts memories, Phase B checks `dreams/dreams.md` for new or updated dream proposals, Phase C rewrites project-flavoured lessons as general rules (project-only facts go to `projects/<name>.md`).
8. **Untested ideas** go to `dreams/` via the `dream-manager` skill, never into `categories/`.
9. Never store secrets, API keys, passwords or personal data in memory.

## Realized dreams
Proven improvements from past work (added by `dream-realizer` Gate 9; detail in `subconscious/`). Newest first.
- DREAM-001 (2026-11-23, passed) — Bash tool halves backslash runs, even in '...' and <<'EOF'; write scripts/JSON with Write, run by path → subconscious/DREAM-001-bash-tool-backslash-layer.md
