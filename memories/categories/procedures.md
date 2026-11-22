# Procedures — validated workflows and reusable processes

Load when: starting a task type listed below.
Format: `## <task type>` then numbered steps, ending with `Validated: YYYY-MM-DD <how>`. Only add a procedure after it has worked at least once.

## Refresh memory from past sessions
1. Write a script (Write tool, scratchpad) that scans `~/.claude/projects/*/*.jsonl` for `tool_result` blocks with `is_error: true`, skipping user rejections.
2. Group by project, dedupe by the first ~60 chars, print a short snippet of each.
3. Turn recurring causes into one-line rules via `memory-optimizer`.
Validated: 2026-11-22 — produced the first issues list in one pass.

## Test a Claude Code hook script locally
1. Write fixture transcripts (`.jsonl`) with the Write tool — not `printf`/heredoc (backslashes get mangled).
2. Pipe `{"transcript_path": "<Windows path>"}` into the script; convert Git Bash paths with `cygpath -m`.
3. Cover: quiet task (no output), noisy task (block JSON), already-handled task (no output), `stop_hook_active: true` (no output).
Validated: 2026-11-22 — kairo `memory-check.cjs`.
