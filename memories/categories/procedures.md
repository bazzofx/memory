# Procedures — validated workflows and reusable processes

Load when: starting a task type listed below.
Format (see `index.md` → Entry format): `## PR-NNN — <task type>`, a `#tags` line, numbered steps, then `Validated: YYYY-MM-DD <how>`. Only add a procedure after it has worked at least once. Scripts a procedure needs go in `C:\ai\toolbox\`.

## PR-001 — Refresh memory from past sessions
#memory #claude-code
1. Write a script (Write tool) that scans `~/.claude/projects/*/*.jsonl` for `tool_result` blocks with `is_error: true`, skipping user rejections. Keep extracts in the session scratchpad (L-001).
2. Group by project, dedupe by the first ~60 chars, print a short snippet of each.
3. Turn recurring causes into one-line rules via `memory-optimizer`.

Validated: 2026-11-22 — produced the first issues list in one pass.

## PR-002 — Test a Claude Code hook script locally
#claude-code #testing
1. Write fixture transcripts (`.jsonl`) with the Write tool, not `printf`/heredoc (backslashes get mangled; I-001, S-007).
2. Pipe `{"transcript_path": "<Windows path>"}` into the script; convert Git Bash paths with `cygpath -m` (I-003).
3. Cover: quiet task (no output), noisy task (block JSON), already-handled task (no output), `stop_hook_active: true` (no output).

Validated: 2026-11-22 — `memory-check.cjs` with fixtures; seen firing live, exactly once, in a C:\ai session on 2026-11-25.
