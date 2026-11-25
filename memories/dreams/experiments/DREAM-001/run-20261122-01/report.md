# DREAM-001 — Realization run report

- Run ID: run-20261122-01
- Date: 2026-11-22
- Requested by: user ("use dream-realizer on dream ID 1")
- Gates reached: 0 (intake) and 1 (recurrence check). Stopped before Gate 2, so there's no experiment plan and nothing was built.
- Outcome: `unconfirmed_after_fix`

## Gate 0 — Intake
- DREAM-001 is still open. It isn't a duplicate, wasn't rejected, and nothing has been deployed. DREAM-002 is the only related dream, it's rejected, and its backslash evidence belongs here.
- Source memory: `categories/issues.md` → "Shell & scripting", first entry (file last written 2026-11-22T22:41:08Z).

## Gate 1 — Does the problem still happen after the rule?
Method: a read-only scan of Claude Code transcripts (`~/.claude/projects/*/*.jsonl`) for messages after 2026-11-22T22:41:08Z. For each Bash call, it checked two things. Does the command match the dream's trigger (heredoc, `printf`, `echo`, `python -c` or `node -e`, with a body containing `\` or `${`)? Did the result have `is_error`? The scanner was written to a file and run by path, which follows the rule itself.

| Scope | Bash calls | Errored | Matched trigger | Matched + errored |
|---|---|---|---|---|
| kairo (4 sessions) | 25 | 2 (both unrelated) | 7 | **0** |
| other projects (5 import-test sessions) | 0 | 0 | 0 | 0 |

Observed evidence:
- None of the 4 original failures has happened since the rule was written.
- The sample is small. It covers about 1 hour of activity, 25 Bash calls and one project with real work. It doesn't show the rule works. It only shows the problem hasn't come back yet.
- The dream's own gate window (2026-11-23 → 2026-12-07) hasn't started, so that scan can't have been done yet.

## Finding that matters for any future hook
The trigger as written matched **7 of 25 (28%) Bash calls that worked fine**: git commit heredocs with a Windows path in the message, `echo "{\"transcript_path\"...}"` test fixtures, and `printf` loops. A hook using that trigger would send far more than the dream's "at most 1 false warning per day" target. If the problem comes back, narrow the trigger first. One candidate: only `python -c` / `node -e` bodies, or heredocs whose output goes into an interpreter (`| node`, `| python`, `> *.py/js/json`), that contain `\\` or `${`. Test that narrower pattern against this same corpus as the false-positive baseline.

## Recommendation
- Keep DREAM-001 pending with status `unconfirmed_after_fix` and monitor.
- After 2026-12-07, run the planned scan again with the scanner logic above (recreate it from this description; don't keep a reusable script, per DREAM-002).
  - If nothing matches and errors → move to Rejected (`resolved_by_memory`).
  - If ≥1 failure matches → go to Gate 2 with the narrowed trigger and this run's 25-call corpus as the false-positive baseline.
- Nothing was installed, and no settings or hooks were changed.
